# Generated by Django 4.1.7 on 2023-03-09 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='search',
            name='zip_code',
            field=models.IntegerField(max_length=10),
        ),
    ]
