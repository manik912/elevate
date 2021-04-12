# Generated by Django 3.0.7 on 2021-04-12 00:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_spot_is_active'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rawmaterial',
            name='cost',
        ),
        migrations.RemoveField(
            model_name='rawmaterial',
            name='quantity',
        ),
        migrations.AddField(
            model_name='spot',
            name='cost',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='spot',
            name='quantity',
            field=models.IntegerField(default=0),
        ),
        migrations.RemoveField(
            model_name='spot',
            name='raw_material',
        ),
        migrations.AddField(
            model_name='spot',
            name='raw_material',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='home.RawMaterial'),
        ),
    ]
