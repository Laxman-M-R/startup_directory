# Generated by Django 3.0.6 on 2020-05-21 10:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0009_auto_20200520_1647'),
    ]

    operations = [
        migrations.RenameField(
            model_name='companyprofile',
            old_name='location',
            new_name='services',
        ),
    ]