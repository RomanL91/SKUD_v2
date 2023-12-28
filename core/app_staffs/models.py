from django.db import models

from app_tag.models import Tags
from app_position.models import Position
from app_departament.models import Departament
from app_access_profile.models import AccessProfile
from app_shedule.models import Schedule

from django.core.validators import RegexValidator


phone_number_regex = RegexValidator(regex = r"^\+7\d{10}$")


class Staff(models.Model):
    first_name = models.CharField(verbose_name='Имя', max_length=50)
    last_name = models.CharField(verbose_name='Фамилия', max_length=150)
    patromic = models.CharField(verbose_name='Отчество', max_length=150, blank=True)

    # --Доступ к территории
    without_biometric_verification = models.BooleanField(
        verbose_name='Открыть доступ без проверки биометрии',
        help_text=  '''Обладатель сможет проходить через проходные без проверки биометрии
                        на проходных где она используется''',
        blank=True, default=False, editable=True #опционально от типа поставки(сейчас отображается)
    )
    access_profile = models.ForeignKey(
        AccessProfile, on_delete=models.CASCADE,
        verbose_name='Профиль доступа', 
    )
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
    departament = models.ForeignKey(
        Departament, on_delete=models.CASCADE,
        verbose_name='Департамент', blank=True, null=True
    )
    position = models.ForeignKey(
        Position, on_delete=models.CASCADE,
        verbose_name='Должость', blank=True, null=True,
    )
    schedule = models.ForeignKey(
        Schedule, on_delete=models.CASCADE,
        verbose_name='Расписание сотрудника', blank=True, null=True
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
    

from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from django.core.cache import cache 


def set_interception(obj, type_oper_card):
    oper_card = {
        "id": 0,
        "operation": "del_cards", # del_cards | add_cards
        "cards": [
            # {"card":"000000A2BA93", "flags": 0, "tz": 255},
        ]
    }
    staff_checkpoint_access_dany = obj.access_profile.checpoint.all()
    staff_sn_controller_access_dany = []

    for checkpoint in staff_checkpoint_access_dany:
        staff_sn_controller_access_dany.extend(
            checkpoint.controller_set.all()
        )
    
    staff_cards = [
        {"card": card.pass_cart_hex_format, "flags": 0, "tz": 255} 
        for card in obj.cardpass_set.all() if card.activate_card
    ]
    oper_card['operation'] = type_oper_card
    oper_card['cards'] = staff_cards
    for contr in staff_sn_controller_access_dany:
        cache.set(contr.serial_number, [oper_card], timeout=15)


@receiver(pre_save, sender=Staff)
def pre_add_staff(sender, instance, *args, **kwargs):
    new_value_interception = instance.interception
    try:
        old_value_interception = Staff.objects.get(pk=instance.pk).interception
    except:
        print(f'[==INFO==] Создание нового сотрудника: {instance}')

    if old_value_interception == new_value_interception:
        print(f'[==INFO==] Без изменения статуса перехвата: {instance}')
    else:
        print(f'[==INFO==] Статус перехвата изменен: {instance}')
        if new_value_interception:
            print(f'[==INFO==] Активирован перехват {instance}')
            set_interception(instance, 'del_cards')
        else:
            print(f'[==INFO==] Отмена перехвата {instance}')
            set_interception(instance, 'add_cards')


# @receiver(post_save, sender=Staff)
# def add_staff(sender, instance, **kwargs):
    # if instance.interception:
        # set_interception(instance, 'del_cards')
    # else:
        # set_interception(instance, 'add_cards')


@receiver(post_delete, sender=Staff)
def delete_staff(sender, instance, **kwargs):
    set_interception(instance, 'del_cards')
