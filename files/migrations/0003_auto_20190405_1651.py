# Generated by Django 2.1.7 on 2019-04-05 16:51

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0002_auto_20190405_1647'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='users',
            field=models.ManyToManyField(editable=False, to=settings.AUTH_USER_MODEL),
        ),
    ]
