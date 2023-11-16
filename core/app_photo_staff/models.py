from os import path

from django.db import models

from app_staffs.models import Staff


def get_path_file(instance, filename):
    # для переименования загружаемых фото
    directory = str(instance.staff.pk)
    filename = f'{instance.staff.pk}.jpeg'
    return path.join('staff_photo', directory, filename)


class StaffPhoto(models.Model):
    photo = models.ImageField(verbose_name='Фотография', blank=True, upload_to=get_path_file)
    desc = models.TextField(verbose_name='Описание', max_length=1500, blank=True)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, verbose_name='Сотрудник')

    # флаг есть ли в системе или нет этого человека....


    class Meta:
            verbose_name = 'Фотография'
            verbose_name_plural = 'Фотографии'


    def __str__(self) -> str:
        return self.staff.last_name
    