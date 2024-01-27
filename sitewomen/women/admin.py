from django.contrib import admin
from .models import Women

# Register your models here.
@admin.register(Women)
class WomenAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'time_create', 'is_published') #Список полей которые будем отображать в админке
    list_display_links = ('id', 'title') #указываем поля на которые можно нажимать (кликабельные)
    ordering = ['time_create', 'title'] # Сортировка записей, если поставил "-" будет в обратном порядке
#admin.site.register(Women, WomenAdmin) лучшая практика, через декоратор