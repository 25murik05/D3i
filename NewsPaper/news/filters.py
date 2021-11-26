from django_filters import FilterSet, DateFromToRangeFilter  # импортируем filterset, чем-то напоминающий знакомые дженерики
from .models import *


class PostFilter(FilterSet):
    time_in = DateFromToRangeFilter()

    class Meta:
        model = Post
        fields = {
            'heading': ['icontains'],
            'author__name': ['exact'],
            'category': ['exact'],

        }
