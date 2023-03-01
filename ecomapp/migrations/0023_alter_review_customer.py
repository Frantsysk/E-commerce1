# Generated by Django 4.1.6 on 2023-03-01 14:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ecomapp', '0022_alter_review_customer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='ecomapp.customer'),
        ),
    ]