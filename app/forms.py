# -*- coding: utf-8 -*-
"""
Definition of forms. Интерфейс между пользователем и сервером
"""

from django.db import models #Для того, чтобы добавить форму ввода комментариев на веб-страницу поста
from django.forms import TextInput, EmailInput

from .models import Comment #отобразить на веб-странице поста все её комментарии
from django import forms
from django.contrib.auth.forms import AuthenticationForm #для аутентификации и авторизации пользователя на сайте Django предоставляет форму класса
from django.utils.translation import gettext_lazy as _
from .models import Blog
from django.contrib.auth.models import User

class FeedbackForm(forms.Form): 
    name = forms.CharField(
        label="Имя",
        min_length=2,
        max_length=100,
        widget=TextInput(
            attrs={
                "class": "form-control",
            }
        )
    )
    email = forms.EmailField(
        label="E-mail",
        required=False,
        widget=EmailInput(
            attrs={
                "class": "form-control",
            },
        )
    )
    rating = forms.ChoiceField(
        label="Оцените сайт",
        choices=[
            ("1", "Плохо"),
            ("2", "Нормально"),
            ("3", "Хорошо"),
            ("4", "Отлично"),
            ("5", "Супер"),
        ],
        widget=forms.RadioSelect,
    )
    improvements = forms.MultipleChoiceField(
        label="Что можно улучшить?",
        choices=[("design", "Дизайн"), ("content", "Контент"), ("usability", "Удобство использования")],
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
    feedback = forms.CharField(
        label="Ваш отзыв",
        widget=forms.Textarea(attrs={"rows": 4, "cols": 40, "class": "form-control",}),
        required=False,
    )

class BootstrapAuthenticationForm(AuthenticationForm): #Отображается данная форма авторизации  на странице "Вход" (файл login.html)
    """Authentication form which uses bootstrap CSS."""
    username = forms.CharField(
        max_length=254,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Имя пользователя'})
    )
    password = forms.CharField(
        label=_("Пароль"),
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
            }
        )
    )


class CommentForm (forms.ModelForm):
    class Meta:
        model = Comment # используемая модель
        fields = ('text',) # требуется заполнить только поле text
        labels = {'text': "Комментарий"} # метка к полю формы text

class BlogForm(forms.ModelForm):
    author = forms.ModelChoiceField(
        queryset=User.objects.all(),
        empty_label="Выберите автора",
        widget=forms.Select(attrs={"class": "form-control"}),
        label="Автор" 
    )

    class Meta:
        model = Blog
        fields = ('title', 'description', 'content', 'image', 'author')
        labels = {
            'title': "Заголовок",
            'description': "Краткое содержание",
            'content': "Полное содержание",
            'image': "Изображение",
            'author': "Автор"
        }