# Generated by Django 4.0.5 on 2022-06-10 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrape', '0002_alter_house_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='house',
            name='bathrooms',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='house',
            name='bedrooms',
            field=models.IntegerField(blank=True),
        ),
    ]
