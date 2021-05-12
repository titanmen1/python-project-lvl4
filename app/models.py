from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(AbstractUser):

    def __str__(self):
        return self.get_full_name()


class Status(models.Model):
    name = models.CharField(_('name'), max_length=64, unique=True)

    def __str__(self):
        return self.name


class Label(models.Model):
    name = models.CharField(_('name'), max_length=64, unique=True)

    def __str__(self):
        return self.name


class Task(models.Model):
    name = models.CharField(_('name'), max_length=64)
    author = models.ForeignKey(get_user_model(), on_delete=models.PROTECT,
                               related_name='author',
                               verbose_name=_('author'))
    executor = models.ForeignKey(get_user_model(), on_delete=models.PROTECT,
                                 related_name='executor',
                                 verbose_name=_('executor'),
                                 blank=True, null=True)
    status = models.ForeignKey(Status, on_delete=models.PROTECT,
                               related_name='status',
                               verbose_name=_('status'))
    labels = models.ManyToManyField(Label, related_name='labels',
                                    verbose_name=_('labels'))
    description = models.TextField(_('description'), blank=True)
    date_create = models.DateTimeField(auto_now_add=True)
    date_finish = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.name
