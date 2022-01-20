# from django.db import models
# from django.contrib.auth.models import User
# from django.db.models import Sum
#
#
# class News(models.Model):
#     title = models.CharField(max_length=50, verbose_name='Заголовок')
#     time_in = models.DateTimeField(auto_now_add=True)
#     text = models.TextField()
#
#     def __str__(self):
#         return '{}'.format(self.title)
#
#     class Meta:
#         verbose_name = 'Новость'
#         verbose_name_plural = 'Новости'

from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.core.cache import cache


class CustomUser(AbstractUser):
    subscribe_category = models.ForeignKey('Category', on_delete=models.CASCADE, null=True, blank=True)


User = get_user_model()


class Author(models.Model):
    name = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return '{}'.format(self.name)

    def update_rating(self):
        postR = self.post_set.aggregate(postRating=Sum('rating'))
        pRat = 0
        pRat += postR.get('postRating')

        comR = self.name.comment_set.aggregate(commentRating=Sum('rating'))
        cRat = 0
        cRat += comR.get('commentRating')

        self.rating = pRat * 3 + cRat
        self.save()


class Category(models.Model):
    category = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return '{}'.format(self.category)


class Post(models.Model):
    news = 'N'
    article = 'A'
    NOA = [
        (news, 'Новости'),
        (article, 'Статьи')
    ]
    noa = models.CharField(max_length=1, choices=NOA, default=news)
    time_in = models.DateTimeField(auto_now_add=True)
    heading = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.IntegerField(default=0)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ManyToManyField(Category, through='PostCategory')

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        if self.rating != 0:
            self.rating -= 1
            self.save()

    def preview(self):
        return self.text[:124] + '...'

    def __str__(self):
        return '{}'.format(self.heading)

    def get_absolute_url(self):  # добавим абсолютный путь, чтобы после создания нас перебрасывало на страницу с товаром
        return f'/news/{self.id}'

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs) # сначала вызываем метод родителя, чтобы объект сохранился
    #     cache.delete(f'post-{self.pk}') # затем удаляем его из кэша, чтобы сбросить его


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return '{}'.format({self.post: self.category})


class Comment(models.Model):
    comment = models.TextField()
    time_in = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    name = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return '{}'.format(self.comment)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        if self.rating != 0:
            self.rating -= 1
            self.save()
