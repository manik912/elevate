# Generated by Django 3.0.7 on 2021-04-11 21:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_rawmaterial_cost'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rawmaterial',
            old_name='amount',
            new_name='quantity',
        ),
    ]
