# Generated by Django 3.0.3 on 2020-09-06 18:39

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=60, unique=True)),
                ('summary', models.CharField(blank=True, max_length=2047)),
                ('document', models.FileField(upload_to='articles/%Y/%m/%d/')),
                ('doctype', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(3)])),
                ('date_creation', models.DateField(auto_now_add=True)),
                ('postmaster', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='account.Account')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag_name', models.CharField(max_length=30)),
                ('tag_article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='article.Article')),
            ],
        ),
        migrations.CreateModel(
            name='ReviewNews',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_RN', models.CharField(max_length=45)),
                ('editor_RN', models.CharField(max_length=45)),
                ('audience_RN', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1)])),
                ('reading_committee_RN', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1)])),
                ('type_RN', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1)])),
                ('pages', models.CharField(blank=True, max_length=20, null=True)),
                ('article', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='article.Article')),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_RP', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(2)])),
                ('num_report', models.CharField(max_length=45)),
                ('article', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='article.Article')),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notif_type', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1)])),
                ('seen', models.BooleanField(default=False)),
                ('sending_date', models.DateField(auto_now_add=True)),
                ('destination', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dest_set', to='account.Account')),
                ('source', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='src_set', to='account.Account')),
                ('topic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='article.Article')),
            ],
        ),
        migrations.CreateModel(
            name='Conference',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_conference', models.CharField(max_length=45)),
                ('editor_conference', models.CharField(max_length=45)),
                ('audience_conference', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1)])),
                ('reading_committee_conference', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1)])),
                ('date_conference', models.DateField()),
                ('location_conference', models.CharField(max_length=45)),
                ('procedding', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1)])),
                ('article', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='article.Article')),
            ],
        ),
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author_name', models.CharField(max_length=40)),
                ('article_ref', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='article.Article')),
                ('user_ref', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='account.Account')),
            ],
        ),
    ]
