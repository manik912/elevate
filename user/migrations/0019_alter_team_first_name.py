# Generated by Django 3.2 on 2021-04-21 22:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0018_auto_20210421_0953'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='first_name',
            field=models.CharField(blank=True, max_length=150, verbose_name='first name'),
        ),
    ]
