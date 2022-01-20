# # from celery import shared_task
# # from .models import *
# # from django.template.loader import render_to_string
# # from django.core.mail import EmailMultiAlternatives
# #
# # @shared_task
# # def news_every_weak():
# #     print('news_every_week_in')
# #     for category in Category.objects.all():
# #         for user in User.objects.all():
# #             if user.subscribe_category == category:
# #                 post = Post.objects.filter(category=category)
# #                 print('news_every_week_if')
# #                 # print(post.heading)
# #                 html_content = render_to_string(
# #                                 'news_weak.html',
# #                                 {
# #                                     'post': post,
# #                                     'category': category,
# #                                     'user': user,
# #                                 }
# #                             )
# #
# #                 msg = EmailMultiAlternatives(
# #                     subject=f'Новые статьи недели! ',
# #                     from_email='murik0525@yandex.ru',
# #                     to=['murik0525@yandex.ru'],
# #                 )
# #                 msg.attach_alternative(html_content, 'text/html')
# #                 print('news_every_week_before_send')
# #                 msg.send()
# #                 print('news_every_week_out')
#
# from celery import shared_task
# import time
#
# @shared_task
# def hello():
#     time.sleep(10)
#     print("Hello, world!")