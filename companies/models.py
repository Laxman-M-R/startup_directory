from django.db import models
from django.contrib.auth.models import User
from custom_cities.models import City
from PIL import Image

class CompanyProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    website_url = models.URLField(max_length=250, default='#')
    logo = models.ImageField(default='default.jpg', upload_to='profile_pics')
    location = models.TextField(blank=True, null=True)
    city = models.ForeignKey(City, models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f'{ self.user.username } Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.logo.path)

        if img.height > 300 or img.width > 300:
            img_output_size = (300, 300)
            img.thumbnail(img_output_size)
            img.save(self.logo.path)

