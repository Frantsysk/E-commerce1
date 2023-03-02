# Generated by Django 4.1.6 on 2023-03-02 14:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ecomapp', '0029_alter_order_payment_method'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='customer_new',
            field=models.ForeignKey(blank=True, default=5, on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='ecomapp.customer'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='paymentmethod',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payment_methods', to='ecomapp.customer'),
        ),
    ]
