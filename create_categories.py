import csv
from companies.models import Category

with open("business_categories.csv", 'r') as file:
    csv_file = csv.DictReader(file)
    for row in csv_file:
        Category.objects.get_or_create(name=dict(row)['Business Category'])
