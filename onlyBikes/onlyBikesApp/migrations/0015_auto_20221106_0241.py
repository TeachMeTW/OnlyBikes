# Generated by Django 3.2.5 on 2022-11-06 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onlyBikesApp', '0014_bikemodel_original_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='bikemodel',
            name='location_rescued',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='bikemodel',
            name='original_owner',
            field=models.CharField(default='rescued', max_length=200),
        ),
    ]
