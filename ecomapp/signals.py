from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Order, OrderProduct


@receiver(post_save, sender=OrderProduct)
def notify_seller(sender, instance, created, **kwargs):
    if created:
        product = instance.product
        seller = product.seller
        subject = 'New Order Notification'
        message = f' Hey {seller.first_name}, you have a new order for {product.name} from someone {instance.order.customer}.'
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=['odessaseller@urknet.com'],
            fail_silently=True,
        )

# @receiver(post_save, sender=OrderProduct)
# def notify_seller(sender, instance, created, **kwargs):
#     if created:
#         print(created, 'created')
#         print(instance, 'instance')
#         print(instance.product, 'instance products')
#         print(instance.order.customer, 'instance customer')
#         print(sender, 'sender')
#         print(kwargs,  'kwargs')
#         send_mail(
#             subject='New sale',
#             message='message',
#             from_email=settings.DEFAULT_FROM_EMAIL,
#             recipient_list=['some email here'],
#             fail_silently=True,
#         )





