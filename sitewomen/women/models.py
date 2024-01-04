from django.db import models
from django.urls import reverse


# Менеджер для моделей (выводит только опубликованные статьи)
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=Women.Status.PUBLISHED)

class Women(models.Model):
    class Status(models.IntegerChoices): # Изменение описания публикации с цифрового формата в строковый
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликовано'

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, db_index=True) # В начале добавить blank=True и default='', после создания удалить и поставить unique=True
    content = models.TextField(blank=True)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(choices=Status.choices, default=Status.DRAFT) # передали choices описания публикации
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, null=True)

    objects = models.Manager()
    published = PublishedManager()
    def __str__(self):
        return self.title

    # Сортировка данных
    class Meta:
        ordering = ['-time_create']
        indexes = [
            models.Index(fields=['-time_create'])
        ]

    def get_absolute_url(self): # формируем url для каждой конкретной записи и возвразаем её
        return reverse('post', kwargs={'post_slug': self.slug})


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.name