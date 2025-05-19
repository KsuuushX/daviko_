"""
Definition of views.
"""
#Для поддержки аутентификации в Django используется модуль django.contrib.auth
from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest
from .forms import BlogForm, FeedbackForm
from django.contrib.auth.forms import UserCreationForm #Для регистрации пользователя
from django.shortcuts import render, redirect #импорт функции render и функции redirect
from django.contrib.auth.models import User #представляют пользователей сайта и используются для проверки прав доступа, регистрации пользователей, ассоциации данных с пользователями
from django.db import models #8
from app.models import Blog #8
from .models import Comment # использование модели комментариев
from .forms import CommentForm # использование формы ввода комментария


def home(request): #функции
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Главная',
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Контакты',
            'message':'Данные для связи',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'О нас',
            'message':'Сведения о нас.',
            'year':datetime.now().year,
        }
    )

def links(request):
   
    resources = [
        {
            'title': 'Популярные бьюти процедуры',
            'url': 'https://sharm72.com/blog/sovety-pokupatelyam/populyarnye-byuti-protsedury/',
            'description': 'Интернет-магазин косметики.',
        },
        {
            'title': 'Ламинирование ресниц',
            'url': 'https://lash.ru/blog/laminirovanie-resnits-chto-eto-i-kak-delayut/',
            'description': 'Если вы не знаете про ламинирование ресниц, что это за процедура, какой эффект она даёт, то это статья для вас.',
        },
        {
            'title': 'Самые эффективные процедуры для восстановления волос',
            'url': 'https://skin.ru/article/samye-jeffektivnye-procedury-dlja-vosstanovlenija-volos/',
            'description': 'Процедуры по восстановлению волос предлагают чуть ли не в каждом салоне, мастера готовы решить любую проблему — стоит лишь провести несколько часов в кресле у парикмахера, и пряди будут как новенькие. Насколько эти обещания соответствуют реальности?',
        },
        ]
    return render(request, 'app/links.html', {'resources': resources, 'title': 'Полезные ресурсы',})

def anketa(request):
    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data  
            return render(request, "app/anketa.html", {"form": None, "data": data})
    else:
        form = FeedbackForm()

    return render(request, "app/anketa.html", {"form": form})

def registration(request): #метод действия контроллера registration для обработки данных и передачи данных с сервера для отображения шаблона веб-страницы регистрации

    """Renders the registration page."""

    assert isinstance(request, HttpRequest)

    if request.method == "POST": # после отправки формы

        regform = UserCreationForm (request.POST)

        if regform.is_valid(): #валидация полей формы

            reg_f = regform.save(commit=False) # не сохраняем автоматически данные формы

            reg_f.is_staff = False # запрещен вход в административный раздел

            reg_f.is_active = True # активный пользователь

            reg_f.is_superuser = False # не является суперпользователем

            reg_f.date_joined = datetime.now() # дата регистрации

            reg_f.last_login = datetime.now() # дата последней авторизации

            reg_f.save() # сохраняем изменения после добавления данных

            return redirect('home') # переадресация на главную страницу после регистрации

    else:

        regform = UserCreationForm() # создание объекта формы для ввода данных нового пользователя

    return render(

        request,

        'app/registration.html',

        {

            'regform': regform, # передача формы в шаблон веб-страницы

            'year':datetime.now().year,

        }

)

def blog(request): #метод действия контроллера blog -8 

    """Renders the blog page."""
    posts = Blog.objects.all() # запрос на выбор всех статей блога из модели

    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/blog.html',

        {
            'title':'Статьи по теме',
            'posts': posts, # передача списка статей в шаблон веб-страницы
            'year':datetime.now().year,
            'is_blog_page': True,
        }   

)

def blogpost(request, parametr):

    """Renders the blogpost page."""
    assert isinstance(request, HttpRequest)
    post_1 = Blog.objects.get(id=parametr) # запрос на выбор конкретной статьи по параметру
    comments = Comment.objects.filter(post=parametr).order_by('-date') # Получаем все комментарии к статье, отсортированные по дате
    
    # Обработка формы для добавления комментария
    if request.method == "POST":
        if request.user.is_authenticated:
            form = CommentForm(request.POST)
            if form.is_valid():
                # Сохраняем комментарий, добавляем недостающие данные
                comment_f = form.save(commit=False)
                comment_f.author = request.user
                comment_f.date = datetime.now()
                comment_f.post = Blog.objects.get(id=parametr)
                comment_f.save()

                return redirect('blogpost', parametr=post_1.id)
        else:
            form = CommentForm()  # Если пользователь не авторизован, форма не отправляется
    else:
        form = CommentForm()  # Пустая форма для нового комментария

    return render(
        request,
        'app/blogpost.html',
        {
            'post_1': post_1, # передача конкретной статьи в шаблон веб-страницы
            'year':datetime.now().year,
            'comments': comments, # передача всех комментариев к данной статье в шаблон веб-страницы
            'form': form, # передача формы добавления комментария в шаблон веб-страницы
        }
)

#@login_required
def newpost(request):
    if not request.user.is_superuser:
        return redirect('blog')

    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)  # Используем форму!
        if form.is_valid():
            form.save()
            return redirect('blog')
    else:
        form = BlogForm()  # Создаём пустую форму

    return render(request, 'app/newpost.html', {'form': form,  'year':datetime.now().year})


def video(request):
    return render (request, 'app/videopage.html',{'year':datetime.now().year})
