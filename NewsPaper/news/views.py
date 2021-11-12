from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView, TemplateView
from .models import *
from django.shortcuts import render
from django.core.paginator import Paginator  # импортируем класс, позволяющий удобно осуществлять постраничный вывод
from .filters import PostFilter  # импортируем недавно написанный фильтр
from .forms import PostForm
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin


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


class NewsListN(ListView):
    model = Post
    template_name = 'news_list.html'
    context_object_name = 'post'
    queryset = Post.objects.filter(noa='N')
    ordering = ['-id']
    paginate_by = 5  # поставим постраничный вывод в один элемент
    # form_class = PostForm

    def get_filter(self):
        return PostFilter(self.request.GET, queryset=super().get_queryset())

    def get_queryset(self):
        return self.get_filter().qs

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['filter'] = self.get_filter()
        # context['categories'] = Category.objects.all()
        # context['form'] = PostForm()
        return context

    # def post(self,request,*args,**kwargs):
    #     form = self.form_class(request.POST)
    #
    #     if form.is_valid():
    #         form.save()
    #
    #     return super().get(request,*args,**kwargs)


class NewsDetailView(DetailView):
    template_name = 'news_detail.html'
    queryset = Post.objects.all()


class NewsCreateView(PermissionRequiredMixin, CreateView):
    template_name = 'news_create.html'
    form_class = PostForm
    permission_required = ('news.add_post',)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = Author.objects.get_or_create(name=self.request.user)[0]
        return super().form_valid(form)


# дженерик для редактирования объекта
class NewsUpdateView(PermissionRequiredMixin, UpdateView):
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


