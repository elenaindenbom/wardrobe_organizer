from django.db import models
from django.contrib.auth import get_user_model
from .outfit import Outfit

User = get_user_model()


class Capsule(models.Model):
    name = models.CharField(
        'Название капсулы',
        max_length=256,
        blank=True,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    outfits = models.ManyToManyField(
        Outfit,
        verbose_name='Комплекты'
    )

    class Meta:
        ordering = ['id']
        verbose_name = 'Капсула'
        verbose_name_plural = 'Капсулы'
        default_related_name = 'capsules'

    def __str__(self):
        if not self.name:
            return f'Капсула {self.id}'
        return self.name
