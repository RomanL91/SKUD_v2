from django import forms

from app_controller.models import Controller


CHOICES_CONTROLLER_ACTIVE = [
    ('0', 'Контроллер выключен'),
    ('1', 'Контроллер включен'),
]

CHOICES_CONTROLLER_ONLINE = [
    ('0', 'Оффлайн'),
    ('1', 'Онлайн'),
]

CHOICES_CONTROLLER_MODE = [
    ('0', 'Норма'),
    ('1', 'Блокировка'),
    ('2', 'Свободный проход'),
    # ('3', 'Ожидание свободного прохода'),
]

CHOICES_CONTROLLER_DIRECTION = [
    ('0', 'Использовать нвстройки контроллера'),
    ('ВХОД', 'Контроллер на ВХОД'),
    ('ВЫХОД', 'Контроллер на ВЫХОД'),
]

class ControllerAdminForm(forms.ModelForm):
    class Meta:
        model = Controller
        widgets = {
            "controller_activity": forms.RadioSelect(choices=CHOICES_CONTROLLER_ACTIVE),
            "controller_online": forms.RadioSelect(choices=CHOICES_CONTROLLER_ONLINE),
            "controller_mode": forms.RadioSelect(choices=CHOICES_CONTROLLER_MODE),
            "direction": forms.RadioSelect(choices=CHOICES_CONTROLLER_DIRECTION),
        }
        fields = '__all__'
