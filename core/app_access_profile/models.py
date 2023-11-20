from django.db import models

from app_checkpoint.models import Checkpoint


class AccessProfile(models.Model):
    name_access_profile = models.CharField(
        verbose_name='Название профиля доступа', max_length=200, unique=True,
        help_text='''
        Придумайте название профиля доступа максимально описавающее его уровень<br>
        доступа на проходные. Например: "Полный доступ" - доступ разрешен через все проходные,<br>
        "Только вход на территорию", "Корпус 99", "Комната 67", "3 этаж", "Ангар 43".<br>
        '''
    )
    desc_access_profile = models.TextField(
        verbose_name='Описание профиля', blank=True
    )
    block_access_profile = models.BooleanField(
        verbose_name='Заблокировать профиль?', default=False,
        help_text='''
        Выбрав данный параметр, все сотрудники, имеющий данный профиль доступа<br>
        не смогут пользоваться своими пропусками на проходных.<br>
        Их пропуска будут стерты из контроллеров, а проходные для них станут не доступны!<br>
        Использовать при явной необходимости, для перехвата большого колличества сотрудников!
        '''
    )
    checpoint = models.ManyToManyField(
        Checkpoint, verbose_name='Проходные',
        help_text='''
        Выбирите проходные, куда данный профиль доступа будет иметь доступ.
        '''
    )


    class Meta:
        verbose_name = 'Профиль доступа'
        verbose_name_plural = 'Профиля доступа'


    def __str__(self) -> str:
        return self.name_access_profile
    