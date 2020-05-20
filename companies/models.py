from django.db import models
from django.contrib.auth.models import User
from custom_cities.models import City, Pincode
from phonenumber_field.modelfields import PhoneNumberField
from PIL import Image

class Category(models.Model):
    name = models.CharField(max_length=250, unique=True)

    def __str__(self):
        return f'{self.name}'

class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=250, unique=True)

    def __str__(self):
        return f'{self.name}'

class CompanyProfile(models.Model):
    DIGITAL_FIELD = 'DF'
    ENGINEERING_FIELD = 'ED'
    LOCAL_BUSINESS = 'LB'
    COMPANY_FIELDS = [
        (DIGITAL_FIELD, 'IT, Consulting and Product Development'),
        (ENGINEERING_FIELD, 'Engineering and Design'),
        (LOCAL_BUSINESS, 'Local Business'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    contact_person = models.CharField(max_length=100, blank=False, null=False, default='Owner')
    contact_number = PhoneNumberField(null=False, blank=False, default='+910123456789')
    website_url = models.URLField(max_length=250, default='#')
    logo = models.ImageField(default='default.jpg', upload_to='profile_pics')
    location = models.TextField(blank=True, null=True)
    address = models.CharField(max_length=500, blank=False, null=False, default='Gandhinagar')
    city = models.ForeignKey(City, models.SET_NULL, blank=True, null=True)
    pincode = models.ForeignKey(Pincode, models.SET_NULL, blank=True, null=True)
    company_field = models.CharField(max_length=100, choices=COMPANY_FIELDS, default=DIGITAL_FIELD)
    company_category = models.ForeignKey(Category, models.SET_NULL, blank=True, null=True)
    company_subcategory = models.ForeignKey(SubCategory, models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f'{ self.user.username } Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.logo.path)

        if img.height > 300 or img.width > 300:
            img_output_size = (300, 300)
            img.thumbnail(img_output_size)
            img.save(self.logo.path)

        

