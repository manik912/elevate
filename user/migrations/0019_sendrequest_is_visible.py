# Generated by Django 3.0.7 on 2021-04-21 23:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0018_auto_20210421_0953'),
    ]

    operations = [
        migrations.AddField(
            model_name='sendrequest',
            name='is_visible',
            field=models.BooleanField(default=False),
        ),
    ]
