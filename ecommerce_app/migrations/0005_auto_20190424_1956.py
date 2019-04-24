# Generated by Django 2.2 on 2019-04-24 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce_app', '0004_auto_20190421_0832'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_type',
            field=models.CharField(choices=[('Subscription', 'SUBSCRIPTION'), ('Product', 'PRODUCT')], default='Subscription', max_length=20),
        ),
        migrations.AddField(
            model_name='order',
            name='payment_status',
            field=models.CharField(choices=[('Processing', 'PROCESSING'), ('Paid', 'PAID'), ('Refused', 'REFUSED'), ('Canceled', 'CANCELED')], default='Processing', max_length=20),
        ),
    ]
