from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import CompanyProfile
from custom_cities.models import City

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

    def __init__(self, *args, **kwargs):
        super(CompanyProfileUpdateForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = CompanyProfile
        fields = ['logo', 'contact_person', 'contact_number', 'company_field', 'company_category', 'company_subcategory', 'address', 'city', 'pincode', 'website_url', 'location']


