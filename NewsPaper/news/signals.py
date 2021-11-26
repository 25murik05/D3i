from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from .models import *
from .views import *
from django.template.loader import render_to_string


@receiver(custom_create_signal, sender=Post)
def notify(sender, instance, created, **kwargs):
    latest_post = instance
    post_category = latest_post.category.all()
    for category in post_category:
        for user in User.objects.all():
            if user.subscribe_category == category:
                html_content = render_to_string(
                    'sub_new_post.html',
                    {
                        'user': user,
                        'category': category,
                        'heading': instance.heading,
                        'text': instance.text,
                        'pk': instance.pk,
                    }
                )

                msg = EmailMultiAlternatives(
                    subject=f'Новая статья: {instance.heading}!',
                    from_email='murik0525@yandex.ru',
                    to=[user.email],
                )
                msg.attach_alternative(html_content, 'text/html')
                msg.send()

@receiver(custom_update_signal, sender=Post)
def notify(sender, instance, created, **kwargs):
    latest_post = instance
    post_category = latest_post.category.all()
    for category in post_category:
        for user in User.objects.all():
            if user.subscribe_category == category:
                html_content = render_to_string(
                        'sub_update_post.html',
                        {
                            'user': user,
                            'category': category,
                            'heading': instance.heading,
                            'text': instance.text
                        }
                    )

                msg = EmailMultiAlternatives(
                    subject=f'Изменение в статье: {instance.heading}!',
                    from_email='murik0525@yandex.ru',
                    to=[user.email],
                )
                msg.attach_alternative(html_content, 'text/html')
                msg.send()
