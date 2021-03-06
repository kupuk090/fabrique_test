# Generated by Django 2.2.10 on 2021-04-18 00:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=4096, verbose_name='Choice text')),
            ],
            options={
                'verbose_name': 'Choice',
                'verbose_name_plural': 'Choices',
            },
        ),
        migrations.CreateModel(
            name='Poll',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=1024, verbose_name='Poll title')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Poll created datetime')),
                ('finished', models.DateField(verbose_name='Poll finished datetime')),
                ('description', models.CharField(max_length=8192, verbose_name='Poll description')),
            ],
            options={
                'verbose_name': 'Poll',
                'verbose_name_plural': 'Polls',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=1024, verbose_name='Title')),
                ('text', models.CharField(max_length=4096, verbose_name='Question text')),
                ('type', models.CharField(choices=[('T', 'Text'), ('C', 'One choice'), ('M', 'Multipal choices')], default='T', max_length=1, verbose_name='Question type')),
            ],
            options={
                'verbose_name': 'Question',
                'verbose_name_plural': 'Questions',
            },
        ),
        migrations.AddConstraint(
            model_name='question',
            constraint=models.CheckConstraint(check=models.Q(type__in=('T', 'C', 'M')), name='%(app_label)s_%(class)s_type_valid'),
        ),
        migrations.AddField(
            model_name='choice',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='choices_set', to='polls.Question'),
        ),
    ]
