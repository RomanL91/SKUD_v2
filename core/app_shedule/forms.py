from django import forms

from app_shedule.models import Schedule, Day


CHOICES_TYPE_SCHEDULE = [
    ('0', 'Расписание проходной'),
    ('1', 'Расписание профиля доступа'),
    ('2', 'Расписание сотрудника'),
]

CHOICES_WEEK_DAY = [
    ('0', 'Понедельник'),
    ('1', 'Вторник'),
    ('2', 'Среда'),
    ('3', 'Четверг'),
    ('4', 'Пятница'),
    ('5', 'Суббота'),
    ('6', 'Воскресенье'),
]


class ScheduleAdminForm(forms.ModelForm):
    class Meta:
        model = Schedule
        widgets = {
            "type_schedule": forms.RadioSelect(choices=CHOICES_TYPE_SCHEDULE),
        }
        fields = '__all__'


class DayAdminForm(forms.ModelForm):
    class Meta:
        model = Day
        widgets = {
            "week_day": forms.Select(choices=CHOICES_WEEK_DAY),
        }
        fields = '__all__'
