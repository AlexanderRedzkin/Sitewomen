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

    title = models.CharField(max_length=255, verbose_name='Заголовок')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='Slug') # В начале добавить blank=True и default='', после создания удалить и поставить unique=True
    content = models.TextField(blank=True, verbose_name='Текст статьи')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время изменения')
    is_published = models.BooleanField(choices=tuple(map(lambda x: (bool(x[0]), x[1]),Status.choices)), default=Status.DRAFT, verbose_name='Статус') # передали choices описания публикации
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, related_name='posts', verbose_name='Категории') # послежним параметром ранее указывали null=True
    tags = models.ManyToManyField('TagPost', blank=True, related_name='tags', verbose_name='Теги')
    husband = models.OneToOneField('Husband', on_delete=models.SET_NULL, null=True, blank=True, related_name='wuman', verbose_name='Муж')

    objects = models.Manager()
    published = PublishedManager()
    def __str__(self):
        return self.title
    # Добавление записей Women.objects.create(title="Ариана Гранде", slug="ariana-grande", cat_id=2)
    # Сортировка данных
    class Meta:
        verbose_name = 'Звёзды' # изменяем название модели в админке
        verbose_name_plural = 'Звёзды' # отображение во множественном числе
        ordering = ['-time_create']
        indexes = [
            models.Index(fields=['-time_create'])
        ]

    def get_absolute_url(self): # формируем url для каждой конкретной записи и возвразаем её
        return reverse('post', kwargs={'post_slug': self.slug})


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name='Категория')
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural= 'Категории'

    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})


class TagPost(models.Model):
    tag = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    def __str__(self):
        return self.tag

    def get_absolute_url(self): #будет возвращать тот или иной адрес для конкретно url адреса
        return reverse('tag', kwargs={'tag_slug': self.slug})

class Husband(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField(null=True)
    m_count = models.IntegerField(blank=True, default=0)

    def __str__(self):
        return self.name
# w1.husband = h1 добавили нового мужа