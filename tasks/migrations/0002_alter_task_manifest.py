# Generated by Django 4.0 on 2021-12-24 01:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='manifest',
            field=models.JSONField(),
        ),
    ]
