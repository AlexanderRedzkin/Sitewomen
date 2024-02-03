from django.contrib import admin
from .models import Women, Category


# Register your models here.
@admin.register(Women)
class WomenAdmin(admin.ModelAdmin):
    list_display = ('title', 'time_create', 'is_published', 'cat', 'brief_info')#для полей которые будут отображаться в админке
    list_display_links = ('title', ) #указываем поля на которые можно нажимать (кликабельные)
    ordering = ['time_create', 'title'] # Сортировка записей, если поставил "-" будет в обратном порядке
#n.site.register(Women, WomenAdmin) лучшая практика, через декоратор
    list_editable = ('is_published', ) #для редактирования записей
    list_per_page = 5
    actions = ['set_published']

    @admin.display(description="Краткое описание", ordering="content")
    def brief_info(self, women: Women):
        return f"Описание {len(women.content)} символов."
    @admin.action(description='Опубликовать выбранные записи')
    def set_published(self, request, queryset):
        queryset.update(is_published=Women.Status.PUBLISHED)
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
