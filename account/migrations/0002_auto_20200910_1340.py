# Generated by Django 3.0.3 on 2020-09-10 12:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='account',
            old_name='facebook',
            new_name='googleScholar',
        ),
        migrations.RemoveField(
            model_name='account',
            name='twitter',
        ),
    ]
