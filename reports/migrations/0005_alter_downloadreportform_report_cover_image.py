# Generated by Django 4.1.8 on 2023-08-14 12:28

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0004_alter_downloadreportform_report_cover_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='downloadreportform',
            name='report_cover_image',
            field=cloudinary.models.CloudinaryField(max_length=255, null=True, verbose_name='image'),
        ),
    ]
