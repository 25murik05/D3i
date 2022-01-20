from django.urls import path
from .views import *
from django.contrib.auth.views import LogoutView
from django.views.decorators.cache import cache_page


urlpatterns = [
    # path('', cache_page(60*1)(NewsListN.as_view())),
    path('', NewsListN.as_view()),
    # path('', NewsList.as_view()),
    # path('<int:pk>', DetailNew.as_view()),
    path('<int:pk>/', NewsDetailView.as_view(), name='news_detail'),  # Ссылка на детали товара
    path('create/', NewsCreateView.as_view(), name='news_create'),
    path('create/<int:pk>', NewsUpdateView.as_view(), name='news_update'),
    path('delete/<int:pk>', NewsDeleteView.as_view(), name='news_delete'),
    path('logout/',
         LogoutView.as_view(template_name='logout.html'),
         name='logout'),
    path('profile/', ProfileView.as_view()),
    path('upgrade/', upgrade_me, name='upgrade'),
    path('category/', SubscribeCategory.as_view()),
    path('text/', Index.as_view())


]