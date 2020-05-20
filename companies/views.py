from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CompanyRegisterForm, CompanyUpdateForm, CompanyProfileUpdateForm
from django.contrib.auth.models import User
from django.db.models import Prefetch
from .models import CompanyProfile
from .snippets import NamePaginator
from custom_cities.models import City, State, Country

def home(request):
    if request.method == 'POST':
        city_id = request.POST.get('city')
        city = City.objects.get(pk=city_id)
        company_field = request.POST.get('company_field')
        companies = User.objects.filter(is_staff=False, companyprofile__city=city, companyprofile__company_field=company_field).prefetch_related(
                                                        Prefetch('companyprofile',
                                                                  queryset = CompanyProfile.objects.filter(city=city_id, company_field=company_field)
                                                        )
                                                    )
    else:
        if request.GET.get('city') and request.GET.get('company_field'):
            city_id = request.GET.get('city')
            city = City.objects.get(pk=city_id)
            company_field = request.GET.get('company_field')
            companies = User.objects.filter(is_staff=False, companyprofile__city=city, companyprofile__company_field=company_field).prefetch_related(
                                                            Prefetch('companyprofile',
                                                                      queryset = CompanyProfile.objects.filter(city=city_id, company_field=company_field)
                                                            )
                                                        )
        else:
            city = City.objects.get(pk=1)
            company_field = 'DF'
            companies = User.objects.filter(is_staff=False, companyprofile__city=1, companyprofile__company_field=company_field).prefetch_related(
                                                                Prefetch('companyprofile',
                                                                          queryset = CompanyProfile.objects.filter(city=1, company_field=company_field)
                                                                )
                                                            )
    cities = City.objects.values('id', 'name')
    company_fields = CompanyProfile.COMPANY_FIELDS
    paginator = NamePaginator(companies, on='username', per_page=25)
    try:
        page = int(request.GET.get('companies', '1'))
    except ValueError:
        page = 1

    try:
        page = paginator.page(page)
    except (InvalidPage):
        page = paginator.page(paginator.num_pages)
    context = { 'companies': page, 'city': city, 'cities': cities, 'company_field':company_field, 'company_fields': company_fields }
    return render(request, 'companies/home.html', context)

def about(request):
    context = { 'title': 'about' }
    return render(request, 'companies/about.html', context)

def register(request):
    if request.method == 'POST':
        form = CompanyRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for { username }!')
            return redirect('login')
    else:
        form = CompanyRegisterForm()
    return render(request, 'companies/register.html', { 'form': form })


@login_required
def profile(request):
    if request.method == 'POST':
        c_form = CompanyUpdateForm(request.POST, instance=request.user)
        cp_form = CompanyProfileUpdateForm(request.POST, request.FILES, instance=request.user.companyprofile)
        if c_form.is_valid() and cp_form.is_valid():
            c_form.save()
            if request.POST['input_city']:
                uncommitted_cp_form = cp_form.save(commit=False)
                co = Country.objects.get_or_create(name=request.POST['input_country'])
                st = State.objects.get_or_create(country=co, name=request.POST['input_state'])
                cit = City.objects.get_or_create(state=st, name=request.POST['input_city'])
                uncommitted_cp_form.city = cit
                uncommitted_cp_form.save()
            else:
                cp_form.save()
            messages.success(request, f'Your profile has been updated!')
            return redirect('profile')
    else:
        c_form = CompanyUpdateForm(instance=request.user)
        cp_form = CompanyProfileUpdateForm(instance=request.user.companyprofile)

    context = {
        'c_form': c_form,
        'cp_form': cp_form
    }

    return render(request, 'companies/profile.html', context)

def city_companies(request):
    return render(request, 'index.html', {'city': city})
