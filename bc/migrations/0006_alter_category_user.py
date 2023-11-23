# Generated by Django 4.2.7 on 2023-11-22 12:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bc', '0005_category_user_alter_category_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
    ]