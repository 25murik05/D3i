import requests
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView, TemplateView, FormView
from .models import *
from django.shortcuts import render
from django.core.paginator import Paginator  # импортируем класс, позволяющий удобно осуществлять постраничный вывод
from .filters import PostFilter  # импортируем недавно написанный фильтр
from .forms import PostForm, CatForm
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.db.models.signals import ModelSignal
from datetime import datetime, date, time
# class NewsListN(ListView):
#     model = Post
#     template_name = 'news.html'
#     context_object_name = 'post'
#     queryset = Post.objects.filter(noa='N')
#
#     # class NewsListPost(ListView):
#     #     model = Post
#     #     template_name = 'news.html'
#     #     context_object_name = 'post'
#     #     queryset = News.objects.order_by('-id').filter(noa='A')
#
#
# class DetailNew(DetailView):
#     model = Post
#     template_name = 'new.html'
#     context_object_name = 'new'
#     queryset = Post.objects.filter(noa='N')

custom_create_signal = ModelSignal(use_caching=True)
custom_update_signal = ModelSignal(use_caching=True)
class NewsListN(ListView):
    model = Post
    template_name = 'news_list.html'
    context_object_name = 'post'
    queryset = Post.objects.filter(noa='N')
    ordering = ['-id']
    paginate_by = 15  # поставим постраничный вывод в один элемент
    # form_class = PostForm

    def get_filter(self):
        return PostFilter(self.request.GET, queryset=super().get_queryset())

    def get_queryset(self):
        return self.get_filter().qs

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['filter'] = self.get_filter()
        return context



class NewsDetailView(DetailView):
    template_name = 'news_detail.html'
    queryset = Post.objects.all()


class NewsCreateView(LoginRequiredMixin, PermissionRequiredMixin,  CreateView):
    template_name = 'news_create.html'
    form_class = PostForm
    permission_required = ('news.add_post',)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = Author.objects.get_or_create(name=self.request.user)[0]
        # user = self.request.user
        all_post_author = self.object.author.post_set.all()
        count_today_post = 0
        for post in all_post_author:
            if post.author == self.object.author:
                time_delta = datetime.now().date() - post.time_in.date()
                if time_delta.total_seconds() < 86400:
                    count_today_post += 1
        if count_today_post < 3:

            self.object.save()
        else:
            return self.handle_no_permission()
        category = Category.objects.get(pk=self.request.POST['category'])
        self.object.category.add(category)
        custom_create_signal.send(sender=Post, instance=self.object, created=True)

        return super().form_valid(form)
        # text = self.object.text
        # heading = self.object.heading
        # if user.subscribe_category == category:
        #     html_content = render_to_string(
        #         'sub_new_post.html',
        #         {
        #             'user': user,
        #             'category': category,
        #             'heading': heading,
        #             'text': text
        #         }
        #     )
        #
        #     msg = EmailMultiAlternatives(
        #         subject=f'Новая статья в категории: {heading}!',
        #         from_email='murik0525@yandex.ru',
        #         to=['murik0525@yandex.ru'],
        #     )
        #     msg.attach_alternative(html_content, 'text/html')
        #     msg.send()



# дженерик для редактирования объекта
class NewsUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    template_name = 'news_create.html'
    form_class = PostForm
    permission_required = ('news.change_post',)

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        author = Author.objects.get(name=user)
        if not author.post_set.filter(pk=kwargs.get('pk')).exists():
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    # метод get_object мы используем вместо queryset, чтобы получить информацию об объекте, который мы собираемся редактировать
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = Author.objects.get_or_create(name=self.request.user)[0]
        # user = self.request.user
        self.object.save()
        category = Category.objects.get(pk=self.request.POST['category'])
        self.object.category.add(category)
        custom_update_signal.send(sender=Post, instance=self.object, created=False)
        return super().form_valid(form)

# дженерик для удаления товара
class NewsDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'news_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        author = Author.objects.get(name=user)
        if not author.post_set.filter(pk=kwargs.get('pk')).exists():
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'profile.html'

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        gr = Group.objects.get(name='common')
        if user.is_authenticated:
            gr.user_set.add(user)
            return super().dispatch(request, *args, **kwargs)
        return self.handle_no_permission()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        return context


@login_required
def upgrade_me(request):
    user = request.user
    premium_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        premium_group.user_set.add(user)
        Author.objects.create(name=user)
    return redirect('/')


class SubscribeCategory(FormView):
    form_class = CatForm
    template_name = 'category.html'
    success_url = '/news/'

    def form_valid(self, form):
        user = self.request.user
        print(user.subscribe_category)
        user.subscribe_category = Category.objects.get(pk=self.request.POST['category'])
        user.save()
        html_content = render_to_string(
            'subscribe_created.html',
            {
                'user': user,
            }
        )

        msg = EmailMultiAlternatives(
            subject='Подписка оформлена!',
            from_email='murik0525@yandex.ru',
            to=[user.email],
        )
        msg.attach_alternative(html_content, 'text/html')
        msg.send()
        return super().form_valid(form)








