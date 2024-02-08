from django.contrib import admin, messages
from .models import Women, Category


# Register your models here.

class MarriedFilter(admin.SimpleListFilter): # В фильтре статус женщины
    title = "Статус женщин"
    parameter_name = "status"

    def lookups(self, request, model_admin):
        return [
            ('married', 'Замужем'),
            ('single', 'Не замужем'),
        ]
    def queryset(self, request, queryset):
        if self.value() == 'married':
            return queryset.filter(husband__isnull=False)
        elif self.value() == 'single':
            return queryset.filter(husband__isnull=True)


@admin.register(Women)
class WomenAdmin(admin.ModelAdmin): # Класс для управления админкой
    fields = ['title', 'slug', 'content', 'cat', 'husband', 'tags'] # поля которые мы можем изменять
    #readonly_fields = ['slug']
    prepopulated_fields = {'slug': ('title', )}# Автоматические заполнение слага при создании
    filter_horizontal = ['tags']
    list_display = ('title', 'time_create', 'is_published', 'cat', 'brief_info')#для полей которые будут отображаться в админке
    list_display_links = ('title', ) #указываем поля на которые можно нажимать (кликабельные)
    ordering = ['time_create', 'title'] # Сортировка записей, если поставил "-" будет в обратном порядке
#n.site.register(Women, WomenAdmin) лучшая практика, через декоратор
    list_editable = ('is_published', ) # для редактирования записей
    list_per_page = 5
    actions = ['set_published', 'set_draft']
    search_fields = ['title', 'cat__name'] # Панель поиска
    list_filter = [MarriedFilter, 'cat__name', 'is_published']# Панель для фильтрации

    @admin.display(description="Краткое описание", ordering="content")
    def brief_info(self, women: Women):
        return f"Описание {len(women.content)} символов."
    @admin.action(description='Опубликовать выбранные записи')
    def set_published(self, request, queryset):
        count = queryset.update(is_published=Women.Status.PUBLISHED)
        self.message_user(request, f'Изменено {count} записей.')

    @admin.action(description='Снять с публикации выбранные записи')
    def set_draft(self, request, queryset):
        count = queryset.update(is_published=Women.Status.DRAFT)
        self.message_user(request, f'{count} записей сняты с публикации!.', messages.WARNING)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
