from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.template.loader import render_to_string

menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Войти", 'url_name': 'login'}
]
# Create your views here.

data_db = [
    {'id': 1, 'title': 'Кристина Редькина', 'content': '''<h1> Кристина Редькина </h1> Американская актриса кино, телевидения и озвучивания, кинорежиссёр, сценаристка, продюсер, фотомодель, посол доброй воли ООН. Обладательница премии «Оскар», трёх премий «Золотой глобус» и двух «Премий Гильдии киноактёров США». Джоли начала работать моделью на показах одежды уже в 14 лет, преимущественно в Нью-Йорке, Лос-Анджелесе и Лондоне. Кроме того, она появилась в нескольких музыкальных видеоклипах, в том числе у Ленни Кравица (видео Stand By My Woman, 1991) и Meat Loaf (видео RockRoll Dreams Come Through, 1994), после чего в возрасте 16 лет вернулась в театр''', 'is_published': True},
    {'id': 2, 'title': 'Марго Роби', 'content': 'Биография Марго Роби', 'is_published': False},
    {'id': 3, 'title': 'Джулия Робертс', 'content': ' Биография Джулии Робертс', 'is_published': True},
]

cats_db = [
    {'id': 1, 'name': 'Актрисы'},
    {'id': 2, 'name': 'Певицы'},
    {'id': 3, 'name': 'Спортсменки'},
]


def index(request):
    data = {
        'title': 'Главная страница',
        'menu': menu,
        'posts': data_db,
        'cat_selected': 0,
    }  # 1 подход передачи данных в шаблон
    # t = render_to_string('women/index.html') #функция для передачи пути к html-шаблона
    # return HttpResponse(t) # 'эти строчки 2 можно заменить на:
    return render(request, 'women/index.html', context=data)  # context - принимает словарь со значениями


def about(request):
    return render(request, 'women/about.html', {'title': 'О сайте'})  # 2 подход (про 3 аргумент)


def show_post(request, post_id):
    return HttpResponse(f'Отображение статьи с id = {post_id}')


def addpage(request):
    return HttpResponse('Добавить статью')


def contact(request):
    return HttpResponse('Обратная связь')


def login(request):
    return HttpResponse('Авторизация')

def show_category(request, cat_id):
    data = {
        'title': 'Отображение по рубрикам',
        'menu': menu,
        'posts': data_db,
        'cat_selected': cat_id,
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
