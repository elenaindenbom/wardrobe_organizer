from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from .item import Item, Purpose


User = get_user_model()


class Outfit(models.Model):
    SA = 'Spring-Autumn'
    SUMMER = 'Summer'
    WINTER = 'Winter'
    UNIVERSAL = 'Universal'
    SEASONS = [
        (SA, 'Весна-Осень'),
        (SUMMER, 'Лето'),
        (WINTER, 'Зима'),
        (UNIVERSAL, 'Универсальный')
    ]
    name = models.CharField(
        'Название комплекта',
        max_length=256,
        blank=True,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    image = models.ImageField(
        'Изображение комплекта',
        upload_to='outfits/',
        blank=True,
    )
    season = models.CharField(
        'Сезон',
        max_length=256,
        choices=SEASONS,
    )
    items = models.ManyToManyField(
        Item,
        verbose_name='Предметы гардероба',
    )
    number_of_uses = models.PositiveSmallIntegerField(
        'Количество использований',
        null=True,
        blank=True,
        default=0,
        validators=(
            MinValueValidator(
                0, message='Количество использований не может быть меньше 0'),
            MaxValueValidator(
                32766,
                message='Количество использований не может быть больше 32766'
            )
        )
    )
    purpose = models.ForeignKey(
        Purpose,
        verbose_name='Область применения',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
    )
    note = models.TextField(
        'Дополнительные заметки',
        blank=True,
    )
    min_temperature = models.SmallIntegerField(
        'Минимальная температура использования в градусах',
        validators=(
            MinValueValidator(
                -50, message='Температура должна быть больше -50 градусов'),
            MaxValueValidator(
                50, message='Температура должна быть меньше 50 градусов')
        )
    )
    max_temperature = models.SmallIntegerField(
        'Максимальная температура использования в градусах',
        validators=(
            MinValueValidator(
                -50, message='Температура должна быть больше -50 градусов'),
            MaxValueValidator(
                50, message='Температура должна быть меньше 50 градусов')
        )
    )

    class Meta:
        ordering = ['-number_of_uses']
        verbose_name = 'Комплект'
        verbose_name_plural = 'Комплекты'
        default_related_name = 'outfits'

    def __str__(self):
        if not self.name:
            return f'Комплект {self.id}'
        return self.name

    def get_absolute_url(self):
        return reverse('wardrobe:outfit_detail', kwargs={'outfit_id': self.pk})


class Use(models.Model):
    outfit = models.ForeignKey(
        Outfit,
        on_delete=models.CASCADE,
        verbose_name='Предмет',
    )
    date = models.DateField(
        'Дата использования',
        auto_now=True,
    )

    class Meta:
        ordering = ['-date']
        verbose_name = 'Информация об использовании'
        verbose_name_plural = 'Информация об использовании'
        default_related_name = 'use'
        constraints = [
            models.UniqueConstraint(fields=['outfit', 'date'],
                                    name='unique_date_use')
        ]

    def __str__(self):
        return self.date.strftime("%m-%d-%Y")
