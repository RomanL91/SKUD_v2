from django.db import models


class Checkpoint(models.Model):
    name_checpoint = models.CharField(
        verbose_name='Имя проходной', max_length=200, unique=True,
        help_text='''
        В данном поле задается имя проходной<br>
        Будьте разумны в наименовании проходных, так как от их имен будете отталкиваться<br>
        отталкиваться в будущем для создания профилей доступа.
        '''
    )
    desc_checkpoint = models.TextField(
        verbose_name='Описание проходной', blank=True,
    )


    class Meta:
        verbose_name = 'Проходная'
        verbose_name_plural = 'Проходные'


    def __str__(self) -> str:
        return self.name_checpoint
    