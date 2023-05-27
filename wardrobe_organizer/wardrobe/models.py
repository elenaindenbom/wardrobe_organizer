from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator


User = get_user_model()


def user_directory_path(instance, filename):
    return f'items/{instance.user.username}/{filename}'


class Purpose(models.Model):
    name = models.CharField(
        'Назначение',
        unique=True,
        max_length=256
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Назначение'
        verbose_name_plural = 'Назначения'

    def __str__(self):
        return self.name


class Type(models.Model):
    TYPE_CATEGORIES = [
        ('Top', 'Верх'),
        ('Bottom', 'Низ'),
        ('Full length', 'Полная длина'),
        ('Outerwear', 'Верхняя одежда'),
        ('Shoes', 'Обувь'),
        ('Accessories', 'Аксессуары'),
        ('Other', 'Другое'),
    ]
    name = models.CharField('Название типа', max_length=256, unique=True)
    category = models.CharField(
        'Категория типа',
        max_length=256,
        choices=TYPE_CATEGORIES,
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Тип'
        verbose_name_plural = 'Типы'

    def __str__(self):
        return self.name


class Care(models.Model):
    recommendation = models.CharField(
        'Рекомендация по уходу',
        max_length=256,
        unique=True,
        blank=True,
    )

    class Meta:
        ordering = ['recommendation']
        verbose_name = 'Рекомендация по уходу'
        verbose_name_plural = 'Рекомендации по уходу'

    def __str__(self):
        return self.recommendation


class Item(models.Model):
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
    name = models.CharField('Название вещи', max_length=256)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    image = models.ImageField(
        'Изображение',
        upload_to=user_directory_path,
    )
    care = models.ManyToManyField(
        Care,
        verbose_name='Рекомендации по уходу',
        blank=True,
    )
    need_to_buy = models.BooleanField(
        'Нужно докупить',
        default=False,
        blank=True,
        null=True,
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
    price = models.PositiveIntegerField(
        'Цена',
        null=True,
        blank=True,
        validators=(
            MinValueValidator(
                0, message='Цена не может быть меньше 0'),
            MaxValueValidator(
                2147483646,
                message='Цена не может быть больше 2147483646'
            )
        )
    )
    season = models.CharField(
        'Сезон',
        max_length=256,
        choices=SEASONS,
    )
    type = models.ForeignKey(
        Type,
        on_delete=models.PROTECT,
        verbose_name='Тип'
    )
    purpose = models.ForeignKey(
        Purpose,
        on_delete=models.PROTECT,
        verbose_name='Назначение',
        null=True,
        blank=True,
    )
    note = models.TextField(
        'Дополнительные заметки',
        blank=True,
    )
    color = models.CharField('Цвет', max_length=256)
    # color_image = models.ImageField(
    #     'Визуализация цвета',
    #     upload_to='color/',
    # )
    storage_place = models.CharField(
        'Место хранения',
        max_length=256,
        blank=True,
        default='Не указано'
    )

    class Meta:
        ordering = ['-number_of_uses']
        verbose_name = 'Предмет гардероба'
        verbose_name_plural = 'Предметы гардероба'
        default_related_name = 'items'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('wardrobe:item_detail', kwargs={'item_id': self.pk})


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
