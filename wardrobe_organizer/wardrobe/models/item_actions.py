from django.db import models
from django.contrib.auth import get_user_model
from .item import Item


User = get_user_model()


class Favorit(models.Model):
    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        verbose_name='В избранном',
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        default_related_name = 'favorits'
        constraints = [
            models.UniqueConstraint(fields=['user', 'item'],
                                    name='unique_favorite')
        ]


class Laundry(models.Model):
    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        verbose_name='В стирке',
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'В стирке'
        verbose_name_plural = 'В стирке'
        default_related_name = 'laundry'
        constraints = [
            models.UniqueConstraint(fields=['user', 'item'],
                                    name='unique_laundry')
        ]
