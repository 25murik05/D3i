from django.urls import path
from .views import *

urlpatterns = [
    path('', NewsListN.as_view()),
    # path('', NewsList.as_view()),
    # path('<int:pk>', DetailNew.as_view()),
    path('<int:pk>/', NewsDetailView.as_view(), name='news_detail'),  # Ссылка на детали товара
    path('create/', NewsCreateView.as_view(), name='news_create'),
    path('create/<int:pk>', NewsUpdateView.as_view(), name='news_update'),
    path('delete/<int:pk>', NewsDeleteView.as_view(), name='news_delete'),
]