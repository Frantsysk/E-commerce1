# Generated by Django 4.1.6 on 2023-03-08 21:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ecomapp', '0036_chat_order_payment_type_reviewreply_message'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReviewReply',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('review', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='reply', to='ecomapp.review')),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='ecomapp.seller')),
            ],
        ),
    ]
