# Generated by Django 4.1.8 on 2023-08-13 21:49

from django.db import migrations
import wagtailcloudinary.fields


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_homepage_dollar_payment_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homepage',
            name='banner_image',
            field=wagtailcloudinary.fields.CloudinaryField(max_length=255, null=True),
        ),
    ]
