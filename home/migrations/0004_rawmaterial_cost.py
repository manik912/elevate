# Generated by Django 3.0.7 on 2021-04-11 21:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_rawmaterial_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='rawmaterial',
            name='cost',
            field=models.IntegerField(default=0),
        ),
    ]
