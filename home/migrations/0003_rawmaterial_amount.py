# Generated by Django 3.0.7 on 2021-04-11 21:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_auto_20210412_0232'),
    ]

    operations = [
        migrations.AddField(
            model_name='rawmaterial',
            name='amount',
            field=models.IntegerField(default=0),
        ),
    ]
