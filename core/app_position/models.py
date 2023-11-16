from django.db import models

from app_tag.models import Tags


class Position(models.Model):
    name_position = models.CharField(
        verbose_name='Название должности', max_length=150,
        unique=True,
    )
    desc_position = models.TextField(
        verbose_name='Описание должности',
    )
    tag = models.ManyToManyField(
        Tags, verbose_name='ТЕГ',
        help_text='''
        Выбирите/добавьте уникальный Тег для должности для создание особых групп.<br>
        Должности могут содержать информацию о разной степени (это категории, разряды и тому подобно).<br>
        За счет Тегов можно обьединить все разряды (Например: монтажник 1р, монтажник 2р), дав им Тег Монтажники.<br>
        <br>
        ''',
        blank=True
    )


    class Meta:
        verbose_name = 'Должность'
        verbose_name_plural = 'Должности'


    def __str__(self) -> str:
        return self.name_position