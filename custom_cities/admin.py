from django.contrib import admin
from .models import City, State, Country, Pincode

admin.site.register(City)
admin.site.register(State)
admin.site.register(Country)
admin.site.register(Pincode)
