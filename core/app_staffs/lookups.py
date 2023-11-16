from django import forms

from app_staffs.models import Staff
from app_position.models import Position

from ajax_select import register, LookupChannel
from ajax_select.fields import AutoCompleteField # or AutoCompleteSelectField


@register('position')
class TagsLookup(LookupChannel):
    model = Position


    def get_query(self, q, request):
        return self.model.objects.filter(name_position__icontains=q).order_by('name_position')[:50]


class StaffModelForm(forms.ModelForm):

    class Meta:
        model = Staff
        fields = '__all__'

    position = AutoCompleteField(
        'position',  show_help_text=False,
        help_text='''Поиск должности<br>Начните ввод названия должности<br>''', 
    )
    