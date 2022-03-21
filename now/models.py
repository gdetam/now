from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils import timezone

from slugify import slugify


class CustomUser(AbstractUser):
    """class CustomUser create structure object user."""

    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=255, verbose_name='Логин', unique=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    email = models.EmailField(max_length=255, verbose_name='Электронная почта')
    password_conf = models.CharField(max_length=255, verbose_name='Подтвержденный пароль')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', verbose_name='Фото', default='logo_profile.png')
    bio = models.TextField(max_length=500, verbose_name='О пользователе', blank=True)
    location = models.CharField(max_length=30, verbose_name='Город', blank=True)
    date_joined = models.DateTimeField(default=timezone.now, verbose_name='Дата регистрации')

    def __str__(self):
        return str(self.username)

    def get_absolute_url(self):
        """Method get_absolute_url return slug for user"""
        return reverse('username', kwargs={'user_slug': self.slug})

    def save(self, *args, **kwargs):
        """Method save create slug for user from username"""
        self.slug = slugify(self.username)
        super(CustomUser, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'now user'
        verbose_name_plural = 'now user'
        ordering = ['id']


class Category(models.Model):
    """class Category create structure object category."""

    category_name = models.CharField(max_length=50, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')

    def __str__(self):
        return str(self.category_name)

    def get_absolute_url(self):
        """Method get_absolute_url return slug for category"""
        return reverse('category', kwargs={'category_slug': self.slug})

    class Meta:
        verbose_name = 'now categories'
        verbose_name_plural = 'now categories'
        ordering = ['id']


class Event(models.Model):
    """class Event create structure object event."""

    title = models.CharField(max_length=255, verbose_name='Название')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    content = models.TextField(blank=False, verbose_name='Описание')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', verbose_name='Фото', default='logo_event.png')
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True, verbose_name='Публикация')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name='Категория')
    user = models.ForeignKey(CustomUser, on_delete=models.PROTECT, verbose_name='Автор')

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        """Method get_absolute_url return slug for event"""
        return reverse('event', kwargs={'event_slug': self.slug})

    def save(self, *args, **kwargs):
        """Method save create slug for event from title"""
        self.slug = slugify(self.title)
        super(Event, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'now events'
        verbose_name_plural = 'now events'
        ordering = ['id', 'time_update', 'title']


class UserJoinEvent(models.Model):
    """class UserJoinEvent create ManyToMany relationships event and user from Event and CustomUser classes."""

    event = models.ForeignKey(Event, on_delete=models.PROTECT, verbose_name='Событие')
    user = models.ForeignKey(CustomUser, on_delete=models.PROTECT, verbose_name='Пользователь')

    def __str__(self):
        return str(self.event) + "\n" + str(self.user)

    class Meta:
        verbose_name = 'now user_join_event'
        verbose_name_plural = 'now user_join_event'
        ordering = ['pk']
