# Generated by Django 4.0.5 on 2022-06-08 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrape', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='house',
            name='price',
            field=models.CharField(max_length=100),
        ),
    ]