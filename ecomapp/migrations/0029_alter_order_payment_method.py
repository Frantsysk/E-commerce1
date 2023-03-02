# Generated by Django 4.1.6 on 2023-03-02 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecomapp', '0028_order_shipping_country_order_shipping_state_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='payment_method',
            field=models.CharField(blank=True, choices=[('Credit', 'Credit Card'), ('Paypal', 'Paypal Account'), ('Apple Pay', 'Apple Pay Account')], default='Credit', max_length=100),
        ),
    ]
