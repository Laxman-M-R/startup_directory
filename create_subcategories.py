import csv
from companies.models import Category, SubCategory

with open("subcategories.csv", 'r') as file:
    csv_file = csv.DictReader(file)
    for row in csv_file:
    	for header, value in row.items():
    		cat = Category.objects.get(name=header)
    		SubCategory.objects.create(category=cat, name=value)