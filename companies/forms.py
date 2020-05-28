from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import CompanyProfile, SubCategory
from custom_cities.models import City, State

class CompanyRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class CompanyUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

class CompanyProfileUpdateForm(forms.ModelForm):
    website_url = forms.URLField(help_text='http://')
    services = forms.CharField(widget=forms.Textarea, help_text='Add each service in next line.')
    state = forms.ModelChoiceField(State.objects.all())

    def __init__(self, *args, **kwargs):
        super(CompanyProfileUpdateForm, self).__init__(*args, **kwargs)
        self.fields['state'].required = False
        self.fields['city'].required = True
        self.fields['website_url'].required = False
        self.fields['address'].required = False
        self.fields['company_subcategory'].queryset = SubCategory.objects.none()
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

        if 'company_category' in self.data:
            try:
                category_id = int(self.data.get('company_category'))
                self.fields['company_subcategory'].queryset = SubCategory.objects.filter(category_id=category_id).order_by('name')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['company_subcategory'].queryset = self.instance.company_category.subcategory_set.order_by('name')

    def clean(self):
        address = self.cleaned_data.get('address')
        website_url = self.cleaned_data.get('website_url')
        if not address and not website_url:
            raise forms.ValidationError('One of fields is required')
        return self.cleaned_data

    class Meta:
        model = CompanyProfile
        fields = ['logo', 'contact_person', 'contact_number', 'company_field', 'company_category', 'company_subcategory', 'address', 'city', 'state', 'pincode', 'website_url', 'services']


