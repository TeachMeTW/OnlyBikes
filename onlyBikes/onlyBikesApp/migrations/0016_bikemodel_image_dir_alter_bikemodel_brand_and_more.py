# Generated by Django 4.1.3 on 2022-11-06 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onlyBikesApp', '0015_auto_20221106_0241'),
    ]

    operations = [
        migrations.AddField(
            model_name='bikemodel',
            name='image_dir',
            field=models.ImageField(default='/bicycle-pictogram.png', upload_to='upload/'),
        ),
        migrations.AlterField(
            model_name='bikemodel',
            name='brand',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='bikemodel',
            name='condition',
            field=models.CharField(choices=[('N', 'New'), ('LN', 'Like-New'), ('U', 'Used')], default='U', max_length=2),
        ),
        migrations.AlterField(
            model_name='bikemodel',
            name='description',
            field=models.CharField(default='', max_length=500),
        ),
        migrations.AlterField(
            model_name='bikemodel',
            name='location',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='bikemodel',
            name='model',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='bikemodel',
            name='price',
            field=models.IntegerField(default=0),
        ),
    ]