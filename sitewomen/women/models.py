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
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, related_name='posts') # послежним параметром ранее указывали null=True
    tags = models.ManyToManyField('TagPost', blank=True, related_name='tags')
    husband = models.OneToOneField('Husband', on_delete=models.SET_NULL, null=True, blank=True, related_name='wuman')

    objects = models.Manager()
    published = PublishedManager()
    def __str__(self):
        return self.title
    # Добавление записей Women.objects.create(title="Ариана Гранде", slug="ariana-grande", cat_id=2)
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