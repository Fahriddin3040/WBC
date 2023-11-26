from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class User(AbstractUser):
    def calculated_balance(self) -> float:
        result = 0

        notes = Operations.objects.filter(user=self)

        for note in notes:
            if note.typ == 1:
                result -= note.amount
            elif note.typ == 2:
                result += note.amount
        return result



@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Operations(models.Model):
    TYP = [
        (1, 'Росход'),
        (2, 'Доход'),
    ]
    user = models.ForeignKey(to='User', on_delete=models.CASCADE, verbose_name='Ползователь')
    category = models.ForeignKey(to='Category', on_delete=models.CASCADE, verbose_name="Категория", default=1)
    typ = models.IntegerField(choices=TYP, verbose_name='Тип')
    amount = models.FloatField(verbose_name='Сумма')
    date_time = models.DateTimeField(auto_now=True, verbose_name='Время создания')




class Category(models.Model):
    title = models.CharField(max_length=125, verbose_name='Название категории:')
    user = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name='Пользователь')

    @staticmethod
    def get_categories(user):
        return Category.objects.filter(user_id=user.id)

    def __str__(self):
        return self.title

