# Generated by Django 2.2.10 on 2021-04-20 14:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0010_auto_20210420_0401'),
    ]

    operations = [
        migrations.RenameField(
            model_name='answer',
            old_name='choice',
            new_name='choices',
        ),
    ]
