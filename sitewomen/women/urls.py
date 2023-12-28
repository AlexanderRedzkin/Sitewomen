from django.urls import path, re_path, register_converter
from . import views
from . import converters

register_converter(converters.FourDigitYearConverter, "year4") # класс конвертора

#Все маршруты которые относятся к приложению women у нас вынесены в отдельный файл
urlpatterns = [
    path('', views.index, name='home'), # 3-ий параметр это имя url куда будет перенаправляться
    path('about/', views.about, name='about'),
    path('addpage/', views.addpage, name='add_page'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login, name='login'),
    path('post/<slug:post_slug>/', views.show_post, name='post'),
    path('category/<int:cat_id>/', views.show_category, name='category'),
    #path(r"archive/<year4:year>/", views.archive, name='archive') # сделали конвертор при помощи класса
    #re_path(r"^archive/(?P<year>[0-9]{4})/", views.archive)  при помощи re_path мы можем сделать свой конвертор
]