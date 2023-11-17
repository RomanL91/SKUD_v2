from django import forms

from app_controller.models import Controller


CHOICES_CONTROLLER_ACTIVE = [
    ('0', 'Контроллер выключен'),
    ('1', 'Контроллер включен'),
]

CHOICES_CONTROLLER_ONLINE = [
    ((0, 0), 'Однофакторный режим'),
    ((1, 1), 'Двухфакторный режим'),
    ((0, 2), 'Свободный проход'),
    ((0, 1), 'Заблокирован'),
]

class ControllerAdminForm(forms.ModelForm):
    class Meta:
        model = Controller
        widgets = {
            "controller_activity": forms.RadioSelect(choices=CHOICES_CONTROLLER_ACTIVE),
            "controller_online": forms.RadioSelect(choices=CHOICES_CONTROLLER_ONLINE),
        }
        fields = '__all__'
