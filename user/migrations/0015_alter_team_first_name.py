# Generated by Django 3.2 on 2021-04-18 00:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0014_auto_20210418_0356'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='first_name',
            field=models.CharField(blank=True, max_length=150, verbose_name='first name'),
        ),
    ]
