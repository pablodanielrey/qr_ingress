# Generated by Django 3.2.7 on 2021-10-22 15:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0002_auto_20211001_1042'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='quizgrade',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='user',
            options={'managed': False},
        ),
    ]
