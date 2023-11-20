from django.db import models
from django.utils.html import format_html
from django.core.validators import RegexValidator


class ColorField(models.CharField):
    """ Поле для хранения HTML-кода цвета."""

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_length', 7)
        super().__init__(*args, **kwargs)
        self.validators.append(RegexValidator(r'#[a-f\d]{6}'))


class Tags(models.Model):
    color_tad = ColorField(
        unique=True, verbose_name='Цвет тега', default='#FF0000',
        )
    name_tag = models.CharField(
        verbose_name='Название тега', max_length=150, unique=True
    )
    desc_tag = models.TextField(
        verbose_name='Описание тега', max_length=1500, blank=True
    )
    interception = models.BooleanField(
        verbose_name='Перехват', default=False,
        help_text='Ограничит доступ данному Тегу на всех проходных/контроллерах'
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


    def __str__(self) -> str:
        return self.name_tag
    