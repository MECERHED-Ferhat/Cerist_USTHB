# Generated by Django 3.0.3 on 2020-09-17 21:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_auto_20200916_2237'),
        ('article', '0002_auto_20200909_0114'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='postmaster',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='account.Account'),
        ),
    ]