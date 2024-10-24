# Generated by Django 4.1.8 on 2024-07-30 01:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0002_registrationformpage_registrationpage_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attendant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_unique_id', models.CharField(max_length=500, unique=True)),
                ('first_name', models.CharField(max_length=255, verbose_name='first name')),
                ('last_name', models.CharField(max_length=255, verbose_name='company')),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('company', models.CharField(blank=True, max_length=255, null=True, verbose_name='company')),
                ('position', models.CharField(blank=True, max_length=255, null=True, verbose_name='position')),
                ('country', models.CharField(blank=True, max_length=255, null=True, verbose_name='country')),
                ('phone', models.CharField(blank=True, max_length=255, null=True, verbose_name='phone')),
            ],
        ),
        migrations.AlterField(
            model_name='user',
            name='company',
            field=models.CharField(blank=True, max_length=255, verbose_name='company'),
        ),
        migrations.AlterField(
            model_name='user',
            name='country',
            field=models.CharField(blank=True, max_length=255, verbose_name='country'),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(blank=True, max_length=255, verbose_name='phone'),
        ),
        migrations.AlterField(
            model_name='user',
            name='position',
            field=models.CharField(blank=True, max_length=255, verbose_name='position'),
        ),
    ]
