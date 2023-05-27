# Generated by Django 3.2.16 on 2023-05-26 21:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wardrobe', '0004_auto_20230527_0007'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='use',
            name='item',
        ),
        migrations.AddField(
            model_name='use',
            name='outfit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='use', to='wardrobe.outfit', unique_for_date=True, verbose_name='Предмет'),
        ),
    ]