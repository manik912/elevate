# Generated by Django 3.0.7 on 2021-04-12 00:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_auto_20210412_0531'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='spot',
            name='cost',
        ),
        migrations.RemoveField(
            model_name='spot',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='spot',
            name='quantity',
        ),
        migrations.RemoveField(
            model_name='spot',
            name='raw_material',
        ),
        migrations.CreateModel(
            name='Resources_on_spot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=0)),
                ('cost', models.IntegerField(default=0)),
                ('is_active', models.BooleanField(default=True)),
                ('raw_material', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='home.RawMaterial')),
                ('spot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.Spot')),
            ],
        ),
    ]
