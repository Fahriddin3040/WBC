# Generated by Django 4.2.7 on 2023-11-22 18:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bc', '0006_alter_category_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='operations',
            name='category',
        ),
    ]
