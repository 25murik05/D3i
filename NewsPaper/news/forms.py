from django.forms import ModelForm, Form
from .models import Post, Category
from django.contrib.auth.models import User
from django import forms
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group


# Создаём модельную форму
class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['heading', 'text', 'category']


class BasicSignupForm(SignupForm):
    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        return user


class CatForm(Form):
    category = forms.ModelChoiceField(queryset=Category.objects.all())

    class Meta:
        fields = ['category']


