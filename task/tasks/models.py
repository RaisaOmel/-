from django.urls import reverse
from django.db import models
from django.contrib.auth.models import User
from datetime import date
class Task(models.Model):
    #  задачи пользователя
    title = models.CharField(max_length=150, verbose_name='Заголовок')
    content = models.TextField(blank=True, verbose_name='Содержание')
    performance = models.DateField(default=date.today, verbose_name='Срок')
    made = models.BooleanField(default=False, verbose_name='Сделано')
    parity = models.BooleanField(default=False, verbose_name='Важно')
    chose = models.BooleanField(default=False, verbose_name='Избрано')
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE, default=1, null=True, blank=True,)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'
        ordering = ['performance', '-parity']
        indexes=[
            models.Index(fields=['performance', '-parity']),
            models.Index(fields=['-parity', 'performance'])
        ]

    def get_absolute_url(self):
        return reverse('edit', kwargs={'pk': self.id})

    objects = models.Manager()

class UserInfo(models.Model):
    # Расширение БД "Пользователи". Т.е. хранится информация по отбору для пользователя

    # хотела отбор сделачть через перечисления. Это расширяла возможности отбора
    # SORT = [(0, 'Срок, срочность'), (1, 'Срочность, срок')]
    # PARITY = [(0, 'Все'), (1, 'Срочно'), (2, 'Несрочно')]
    # MADES = [(0, 'Все'), (1, 'Невыполнено'), (2, 'Выполнено')]
    # CHOSE = [(0, 'Все'), (1, 'Избрано'), (2, 'Неизбрано')]
    # SELECTE = [(0, 'Все'), (1, 'Текст'), (2, 'Дата')]
    #
    # user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE, default=1)
    # sorted = models.BooleanField(choices=SORT,default=False, verbose_name='Сортировка') # 0 (срок,паритет);  1 (паритет, срок)
    # made = models.IntegerField(choices=MADES,default=0, verbose_name='Сделано') # 0-все; 1-не выполнено; 2-выполнено
    # parity = models.IntegerField(choices=PARITY,default=0, verbose_name='Срочно') # 0-все; 1-важные; 2- не важные
    # chose = models.IntegerField(choices=CHOSE,default=0, verbose_name='Избрано') # 0-все; 1-избранные; 2-не избранные
    # selection = models.IntegerField(choices=SELECTE,default=0, verbose_name='Отбор') #0-все; 1-отбор по сроку; 2-отбор по ключу
    # selection_date = models.DateField(null=True, blank=True,verbose_name='Отбор по сроку')
    # selection_key = models.CharField(max_length=150, null=True, blank=True, verbose_name='Отбор по ключу')

    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE, default=1, null=True, blank=True,)
    sorted = models.BooleanField(default=False, verbose_name='Сортировка') # 0 (срок,паритет);  1 (паритет, срок)
    made = models.BooleanField(default=False, verbose_name='Сделано') # 0-все; 1-не выполнено; 2-выполнено
    parity = models.BooleanField(default=False, verbose_name='Срочно') # 0-все; 1-важные; 2- не важные
    chose = models.BooleanField(default=False, verbose_name='Избрано') # 0-все; 1-избранные; 2-не избранные
    selection = models.BooleanField(default=False, verbose_name='Отбор') #0-все; 1-отбор по сроку; 2-отбор по ключу
    selection_key = models.CharField(max_length=150, null=True, blank=True, verbose_name='Отбор по ключу')

    def __str__(self):
        return str(self.user)+"//"+str(self.sorted)+"//"+str(self.made)+"//"+str(self.parity)+"//"+str(self.chose)\
            +"//"+str(self.selection)+"//"+str(self.selection_key).strip()

    class Meta:
        ordering = ['-user']

    objects = models.Manager()