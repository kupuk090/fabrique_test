# Generated by Django 2.2.10 on 2021-04-18 16:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0006_auto_20210418_1620'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='title',
        ),
    ]
