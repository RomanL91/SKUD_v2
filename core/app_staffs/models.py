from django.db import models

from app_tag.models import Tags
from app_position.models import Position

from django.core.validators import RegexValidator


phone_number_regex = RegexValidator(regex = r"^\+7\d{10}$")


class Staff(models.Model):
    # --Данные о сотруднике
    first_name = models.CharField(verbose_name='Имя', max_length=50)
    last_name = models.CharField(verbose_name='Фамилия', max_length=150)
    patromic = models.CharField(verbose_name='Отчество', max_length=150, blank=True)

    # --Фото
    # ФОТО(много - 3 к примеру)
    # Пропускать без проверки биометриии
        #опциаонально поле в зависимоти от комплектации
    without_biometric_verification = models.BooleanField(
        verbose_name='Открыть доступ без проверки биометрии',
        help_text=  '''Обладатель сможет проходить через проходные без проверки биометрии
                        на проходных где она используется''',
        blank=True, default=False, editable=True #опционально от типа поставки(сейчас отображается)
    )

    # --Доступ к территории
    # профиль доступа
    # перехват
    interception = models.BooleanField(
        verbose_name='Перехват', default=False,
        help_text='Ограничит доступ на всех проходных/контроллерах'
    )

    # --Спец теги для группировки сотрудников по какому либо признаку
    tag = models.ManyToManyField(
        Tags, verbose_name='ТЕГ', 
        help_text='''
        Выбирите/добавьте уникальный Тег для сотрудника для создание особых групп сотрудников.<br>
        Добавляйте сотруднику сколько угодно Тегов, включая его в разные группы.<br><br>
        ''',
        blank=True)
    
    # --Информация о рабочем статусе
    # департамент
    # должность
    position = models.ForeignKey(
        Position, on_delete=models.CASCADE,
        verbose_name='Долность', blank=True, null=True,
    )
    # график сотрудника

    # --Остальное о сотруднике
    phone_number = models.CharField(
        verbose_name='Телефонный номер', max_length=12,
        validators=[phone_number_regex,], blank=True
    )
    home_adress = models.CharField(
        verbose_name='Домашний адресс', max_length=300, blank=True
    )


    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'


    def __str__(self) -> str:
        return self.last_name
