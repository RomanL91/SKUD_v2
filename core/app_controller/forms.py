from django import forms

from app_controller.models import Controller


CHOICES_CONTROLLER_ACTIVE = [
    ('0', 'Контроллер выключен'),
    ('1', 'Контроллер включен'),
]

CHOICES_CONTROLLER_ONLINE = [
    ('0/0', 'Однофакторный режим'),
    ('1/1', 'Двухфакторный режим'),
    ('0/2', 'Свободный проход'),
    ('0/1', 'Заблокирован'),
]

CHOICES_CONTROLLER_DIRECTION = [
    ('0', 'Контроллер на ВХОД и ВЫХОД'),
    ('1', 'Контроллер на ВХОД'),
    ('2', 'Контроллер на ВЫХОД'),
]

class ControllerAdminForm(forms.ModelForm):
    class Meta:
        model = Controller
        widgets = {
            "controller_activity": forms.RadioSelect(choices=CHOICES_CONTROLLER_ACTIVE),
            "controller_online": forms.RadioSelect(choices=CHOICES_CONTROLLER_ONLINE),
            "direction": forms.RadioSelect(choices=CHOICES_CONTROLLER_DIRECTION),
        }
        fields = '__all__'
