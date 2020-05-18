import csv
from custom_cities.models import Country, City, State

with open("indian_cities.csv", 'r') as file:
    csv_file = csv.DictReader(file)
    for row in csv_file:
        s = State.objects.get_or_create(country=Country.objects.all().first(), name=dict(row)['State'])
        City.objects.get_or_create(state=s[0], name=dict(row)['City'])
