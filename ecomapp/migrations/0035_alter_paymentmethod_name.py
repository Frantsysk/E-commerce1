# Generated by Django 4.1.6 on 2023-03-03 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecomapp', '0034_alter_paymentmethod_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentmethod',
            name='name',
            field=models.CharField(max_length=50),
        ),
    ]
