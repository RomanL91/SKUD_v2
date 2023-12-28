from django.db import models


class Departament(models.Model):
    name_departament = models.CharField(
        verbose_name='Департамент', unique=True, max_length=200
    )
    desc_dep = models.TextField(
        verbose_name='Описание', blank=True
    )
    # Убираем данный функционал на данный момент    
    # interception = models.BooleanField(
    #     verbose_name='Перехват', default=False,
    #     help_text='''Ограничит доступ на всех проходных/контроллерах сотрудников<br>
    #     принадлежащие к данному Департаменту'''
    # )


    class Meta:
        verbose_name = 'Департамент'
        verbose_name_plural = 'Департаменты'


    def __str__(self) -> str:
        return self.name_departament
    