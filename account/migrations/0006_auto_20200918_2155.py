# Generated by Django 3.0.3 on 2020-09-18 20:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_auto_20200918_1820'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='profile_pic',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='profiles_pics/'),
        ),
    ]
