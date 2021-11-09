from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from .models import *
from django.shortcuts import render
from django.core.paginator import Paginator  # импортируем класс, позволяющий удобно осуществлять постраничный вывод
from .filters import PostFilter  # импортируем недавно написанный фильтр
from .forms import PostForm


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
    paginate_by =  5 # поставим постраничный вывод в один элемент
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


class NewsCreateView(CreateView):
    template_name = 'news_create.html'
    form_class = PostForm


# дженерик для редактирования объекта
class NewsUpdateView(UpdateView):
    template_name = 'news_create.html'
    form_class = PostForm

    # метод get_object мы используем вместо queryset, чтобы получить информацию об объекте, который мы собираемся редактировать
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


# дженерик для удаления товара
class NewsDeleteView(DeleteView):
    template_name = 'news_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'