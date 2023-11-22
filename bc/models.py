from enum import property
from django.contrib.auth.hashers import make_password
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from rest_framework.routers import Response
import hashlib
import binascii
import os


class User(AbstractUser):

    def calculated_balance(self) -> float:
        result = 0

        notes = Operations.objects.filter(user=self)

        for note in notes:
            if note.category == 1:
                result -= note.amount
            else:
                result += note.amount
        return result



@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Operations(models.Model):
    TYPE = [
        (1, 'Росход'),
        (2, 'Доход'),
    ]
    user = models.ForeignKey(to='User', on_delete=models.CASCADE, verbose_name='Ползователь')
    category = models.ForeignKey(to='Category', on_delete=models.CASCADE, verbose_name="Категория")
    type = models.IntegerField(choices=TYPE, verbose_name='Тип')
    amount = models.FloatField(verbose_name='Сумма')
    date_time = models.DateTimeField(auto_now=True, verbose_name='Время создания')


class Category(models.Model):
    title = models.CharField(max_length=125, verbose_name='Название категории:')
    user = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name='Пользователь')

    def __str__(self):
        return self.title


