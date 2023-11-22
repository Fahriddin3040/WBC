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
    password_row = models.CharField(max_length=35)
    is_active = True


    def set_p(self):
        return make_password(self.password_row)

    def save(self, *args, **kwargs):
        self.password = self.set_p()
        super().save(*args, **kwargs)

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
    category = [
        (1, 'Росход'),
        (2, 'Доход'),
    ]
    user = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name='Ползователь')
    category = models.IntegerField(choices=category, verbose_name='Категория')
    reason = models.CharField(max_length=75, verbose_name='Причина')
    amount = models.IntegerField(verbose_name='Финансовая стоимость')
    date_time = models.DateTimeField(auto_now=True, verbose_name='Время создания')




