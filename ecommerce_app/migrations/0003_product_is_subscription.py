# Generated by Django 2.2 on 2019-04-21 07:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce_app', '0002_auto_20181206_1406'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='is_subscription',
            field=models.BooleanField(default=True),
        ),
    ]
