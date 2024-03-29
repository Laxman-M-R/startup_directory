# Generated by Django 3.0.6 on 2020-05-20 16:47

from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('custom_cities', '0002_pincode'),
        ('companies', '0008_companyprofile_company_field'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='companyprofile',
            name='address',
            field=models.CharField(default='Gandhinagar', max_length=500),
        ),
        migrations.AddField(
            model_name='companyprofile',
            name='contact_number',
            field=phonenumber_field.modelfields.PhoneNumberField(default='+910123456789', max_length=128, region=None),
        ),
        migrations.AddField(
            model_name='companyprofile',
            name='contact_person',
            field=models.CharField(default='Owner', max_length=100),
        ),
        migrations.AddField(
            model_name='companyprofile',
            name='pincode',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='custom_cities.Pincode'),
        ),
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, unique=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='companies.Category')),
            ],
        ),
        migrations.AddField(
            model_name='companyprofile',
            name='company_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='companies.Category'),
        ),
        migrations.AddField(
            model_name='companyprofile',
            name='company_subcategory',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='companies.SubCategory'),
        ),
    ]
