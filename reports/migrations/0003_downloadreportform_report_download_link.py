# Generated by Django 4.1.8 on 2023-05-10 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0002_remove_downloadreportform_intro_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='downloadreportform',
            name='report_download_link',
            field=models.URLField(blank=True, null=True),
        ),
    ]
