from django.db import models


class User(models.Model):
    
    f_name = models.CharField(max_length=25)
    l_name = models.CharField(max_length=25)
    email = models.EmailField(max_length=38, verbose_name='Электронный адрес почты')
    
    def __str__(self):
        return f'{self.f_name} {self.l_name}'
    

class Note(models.Model):
    CATEGORIES_OF_TRANSACTION = [
        (1, 'Расход'),
        (2, 'Доход'),
    ]

    user = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name='Пользователь')
    category = models.IntegerField(choices=CATEGORIES_OF_TRANSACTION)
    reason = models.CharField(max_length=60, verbose_name='Причина')
    price = models.IntegerField(verbose_name='Финансовая стоимость')
    date_time = models.DateTimeField(auto_now=True, verbose_name='Дата и время')

    def __str__(self):
        return self.reason


