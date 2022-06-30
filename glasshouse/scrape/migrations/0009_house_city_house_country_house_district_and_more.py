# Generated by Django 4.0.5 on 2022-06-30 04:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrape', '0008_alter_pricehistory_house_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='house',
            name='city',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='house',
            name='country',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='house',
            name='district',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='house',
            name='price',
            field=models.FloatField(),
        ),
    ]
