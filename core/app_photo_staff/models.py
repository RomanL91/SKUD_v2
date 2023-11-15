from django.db import models

from app_staffs.models import Staff


class StaffPhoto(models.Model):
    photo = models.ImageField(verbose_name='Фотография', blank=True, upload_to='staff_photo/')
    desc = models.TextField(verbose_name='Описание', max_length=1500, blank=True)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, verbose_name='Сотрудник')

    class Meta:
            verbose_name = 'Фотография'
            verbose_name_plural = 'Фотографии'


    def __str__(self) -> str:
        return self.staff.last_name