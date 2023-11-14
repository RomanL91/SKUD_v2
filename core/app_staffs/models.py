from django.db import models

from django.core.validators import RegexValidator


phone_number_regex = RegexValidator(regex = r"^\+7\d{10}$")


class Staff(models.Model):
    # --Данные о сотруднике
    first_name = models.CharField(verbose_name='Имя', max_length=50)
    last_name = models.CharField(verbose_name='Фамилия', max_length=150)
    patromic = models.CharField(verbose_name='Отчество', max_length=150, blank=True)

    # --Данные о номере пропуска
    # pass_card_dec_format = models.CharField(
    #     verbose_name='Номер пропуска в DEC формате', max_length=10, unique=True
    # )
    # pass_cart_hex_format = models.CharField(
    #     verbose_name='Номер пропуска в HEX формате', max_length=10, unique=True
    # )

    # --Фото
    # ФОТО(много - 3 к примеру)
    # Пропускать без проверки биометриии
        #опциаонально поле в зависимоти от комплектации

    # --Доступ к территории
    # профиль доступа
    # перехват
    interception = models.BooleanField(
        verbose_name='Перехват', default=False,
        help_text='Ограничит доступ на всех проходных/контроллерах'
    )

    # --Спец теги для группировки сотрудников по какому либо признаку
    # теги
    
    # --Информация о рабочем статусе
    # департамент
    # должность
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
