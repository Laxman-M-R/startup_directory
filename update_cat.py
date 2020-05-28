from companies.models import Category, SubCategory, CompanyProfile

cps = CompanyProfile.objects.all()

for cp in cps:
    if cp.id % 2 == 0:
        comcat = Category.objects.get(pk=17)
        subcat = comcat.subcategory_set.first()
        cp.company_category = comcat 
        cp.company_subcategory = subcat
        cp.save()
    elif cp.id % 3 == 0:
        comcat = Category.objects.get(pk=21)
        subcat = comcat.subcategory_set.first()
        cp.company_category = comcat
        cp.company_subcategory = subcat
        cp.save()
    elif cp.id % 7 == 0:
        comcat = Category.objects.get(pk=9)
        subcat = comcat.subcategory_set.first()
        cp.company_category = comcat
        cp.company_subcategory = subcat
        cp.save()