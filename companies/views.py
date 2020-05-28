from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CompanyRegisterForm, CompanyUpdateForm, CompanyProfileUpdateForm
from django.contrib.auth.models import User
from django.db.models import Prefetch
from .models import CompanyProfile, Category, SubCategory
from .snippets import NamePaginator
from custom_cities.models import Pincode, City, State, Country

def home(request):
    if request.method == 'POST':
        city_id = request.POST.get('city')
        city = City.objects.get(pk=city_id)
        company_field = request.POST.get('company_field')
        category_id = request.POST.get('category')
        category = Category.objects.get(pk=category_id)
        companies = User.objects.filter(is_staff=False, companyprofile__city=city, companyprofile__company_category=category).prefetch_related(
                                                        Prefetch('companyprofile',
                                                                  queryset = CompanyProfile.objects.filter(city=city_id, company_category_id=category_id)
                                                        )
                                                    )
    else:
        if request.GET.get('city') and request.GET.get('category'):
            city_id = request.GET.get('city')
            city = City.objects.get(pk=city_id)
            category_id = request.GET.get('category')
            category = Category.objects.get(pk=category_id)
            companies = User.objects.filter(is_staff=False, companyprofile__city=city, companyprofile__company_category=category).prefetch_related(
                                                            Prefetch('companyprofile',
                                                                      queryset = CompanyProfile.objects.filter(city=city_id, company_category_id=category_id)
                                                            )
                                                        )
        else:
            city = City.objects.get(pk=1)
            company_field = 'DF'
            category = Category.objects.first()
            companies = User.objects.filter(is_staff=False, companyprofile__city=1, companyprofile__company_category=category).prefetch_related(
                                                                Prefetch('companyprofile',
                                                                          queryset = CompanyProfile.objects.filter(city=1, company_category=category)
                                                                )
                                                            )
    cities = City.objects.values('id', 'name')
    company_fields = CompanyProfile.COMPANY_FIELDS
    categories = Category.objects.all()
    paginator = NamePaginator(companies, on='username', per_page=25)
    try:
        page = int(request.GET.get('companies', '1'))
    except ValueError:
        page = 1

    try:
        page = paginator.page(page)
    except (InvalidPage):
        page = paginator.page(paginator.num_pages)
    context = { 'companies': page, 'city': city, 'cities': cities, 'categories': categories, 'category': category }
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
    pincode = request.user.companyprofile.pincode.pincode if request.user.companyprofile.pincode else ''
    if request.method == 'POST':
        c_form = CompanyUpdateForm(request.POST, instance=request.user)
        cp_form = CompanyProfileUpdateForm(request.POST, request.FILES, instance=request.user.companyprofile)
        if c_form.is_valid() and cp_form.is_valid():
            c_form.save()
            uncommitted_cp_form = cp_form.save(commit=False)
            if request.POST['city']:
                pin = Pincode.objects.get_or_create(city_id=request.POST['city'], pincode=request.POST['input_pincode'])[0]
                uncommitted_cp_form.pincode = pin
            if request.POST['input_city']:                
                st = State.objects.get(name=request.POST['input_state'])
                cit = City.objects.get_or_create(state=st, name=request.POST['input_city'])[0]
                pin = Pincode.objects.get_or_create(city=cit, pincode=request.POST['input_pincode'])[0]
                uncommitted_cp_form.city = cit
                uncommitted_cp_form.pincode = pin
            if request.POST['input_company_category'] or request.POST['input_company_subcategory']:
                com_cat = Category.objects.get_or_create(name=request.POST['input_company_category'])[0]
                import ipdb; ipdb.set_trace()
                com_subcat = SubCategory.objects.get_or_create(category=com_cat, name=request.POST['input_company_subcategory'])[0]
                uncommitted_cp_form.company_category = com_cat
                uncommitted_cp_form.company_subcategory = com_subcat
            uncommitted_cp_form.save()
            pincode = request.user.companyprofile.pincode.pincode
            messages.success(request, f'Your profile has been updated!')
            return redirect('profile')
    else:
        c_form = CompanyUpdateForm(instance=request.user)
        cp_form = CompanyProfileUpdateForm(instance=request.user.companyprofile)
    context = {
        'c_form': c_form,
        'cp_form': cp_form,
        'pincode': pincode
    }
    return render(request, 'companies/profile.html', context)

def load_subcategories(request):
    category_id = request.GET.get('company_category')
    sub_categories = SubCategory.objects.filter(category_id=category_id).order_by('name')
    return render(request, 'companies/subcategory_dropdown_list_options.html', {'sub_categories': sub_categories})