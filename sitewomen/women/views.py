from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.template.loader import render_to_string

from .forms import AddPostForm
from .models import Women, Category, TagPost

menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Войти", 'url_name': 'login'}
]
# Create your views here.



def index(request):
    posts = Women.published.all().select_related('cat') #Все опубликованные статьи

    data = {
        'title': 'Главная страница',
        'menu': menu,
        'posts': posts,
        'cat_selected': 0,
    }
    # 1 подход передачи данных в шаблон
    # t = render_to_string('women/index.html') #функция для передачи пути к html-шаблона
    # return HttpResponse(t) # 'эти строчки 2 можно заменить на:
    return render(request, 'women/index.html', context=data)  # context - принимает словарь со значениями


def about(request):
    return render(request, 'women/about.html', {'title': 'О сайте'})  # 2 подход (про 3 аргумент)


def show_post(request, post_slug):
    post = get_object_or_404(Women, slug=post_slug) # функция возвращает одину запись из таблицы, либо генерит исключение

    data = {
        'title': post.title,
        'menu': menu,
        'post': post,
        'cat_selected': 1,
    }

    return render(request, 'women/post.html', data)


def addpage(request):
    if request.method == 'POST': # Если форма была передана по POST запросу
        form = AddPostForm(request.POST) # то мы формируем объект класса AddPostForm
        if form.is_valid(): # проверяем данные
            #print(form.cleaned_data)
            try:
                Women.objects.create(**form.cleaned_data)
                return redirect('home')
            except:
                form.add_error(None, "Ошибка добавления поста")

    else: # Если обычный GЕТ запрос
        form = AddPostForm() # мы формируем объект этого класса, но с пустыми полями

    data = {
        'menu': menu,
        'title': 'Добавление статьи',
        'form': form
    }
    return render(request, 'women/addpage.html', data)


def contact(request):
    return HttpResponse('Обратная связь')


def login(request):
    return HttpResponse('Авторизация')

def show_category(request, cat_slug):
    category = get_object_or_404(Category, slug=cat_slug)
    posts = Women.published.filter(cat_id=category.pk).select_related("cat")

    data = {
        'title': f'Рубрика: {category.name}',
        'menu': menu,
        'posts': posts,
        'cat_selected': category.pk,
    }
    return render(request, 'women/index.html', context=data)

# def archive(request, year):
#    if year > 2023:
#        uri = reverse('cats', args=('music',)) # если в адресе url есть конверторы их нужно передать в args, этот способ альтернативен return redirect('cats', 'music')
#        return redirect(uri) #Рекомендуемая практика использовать имена redirect('home') для перенаправления (redirect) или использовать классы HttpResponceRedict() - 302, HttpResponcePermanentRedict() - 301
# return redirect('cats', 'music')
# return HttpResponceRedict(uri)
#    return HttpResponse(f"<h1>Архив по годам</h1><p>year: {year}</p>")

def page_not_found(request, exception):  # представление обрабатыващее исключение
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")

def show_tag_postlist(request, tag_slug):
    tag = get_object_or_404(TagPost, slug=tag_slug)
    posts = tag.tags.filter(is_published=Women.Status.PUBLISHED).select_related("cat") #получаем все записи связанные с этим тегом

    data = {
        'title': f"Тег: {tag.tag}",
        'menu': menu,
        'posts': posts,
        'cat_selected': None,
    }

    return render(request, 'women/index.html', context=data)