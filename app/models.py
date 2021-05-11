from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from django.utils import timezone


class Status(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class Label(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class Task(models.Model):
    name = models.CharField(max_length=64)
    author = models.ForeignKey(User, on_delete=models.PROTECT, related_name='author')
    executor = models.ForeignKey(User, on_delete=models.PROTECT, related_name='executor', blank=True, null=True)
    status = models.ForeignKey(Status, on_delete=models.PROTECT, related_name='status')
    labels = models.ManyToManyField(Label, related_name='labels')
    description = models.TextField()
    date_create = models.DateTimeField(auto_now_add=True)
    date_finish = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.name
