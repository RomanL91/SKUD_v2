from django import forms

from app_shedule.models import Day


# CHOICES_TYPE_SCHEDULE = [
#     ('Расписание проходной', 'Расписание проходной'),
#     ('Расписание профиля', 'Расписание профиля'),
#     ('Расписание сотрудника', 'Расписание сотрудника'),
# ]

CHOICES_WEEK_DAY = [
    ('Понедельник', 'Понедельник'),
    ('Вторник', 'Вторник'),
    ('Среда', 'Среда'),
    ('Четверг', 'Четверг'),
    ('Пятница', 'Пятница'),
    ('Суббота', 'Суббота'),
    ('Воскресенье', 'Воскресенье'),
]


# class ScheduleAdminForm(forms.ModelForm):
#     class Meta:
#         model = Schedule
#         widgets = {
#             "type_schedule": forms.RadioSelect(choices=CHOICES_TYPE_SCHEDULE),
#         }
#         fields = '__all__'


class DayAdminForm(forms.ModelForm):
    class Meta:
        model = Day
        widgets = {
            "week_day": forms.Select(choices=CHOICES_WEEK_DAY),
        }
        fields = '__all__'
