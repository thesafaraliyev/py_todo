# Generated by Django 3.0.5 on 2020-04-27 14:44

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0002_auto_20200424_2345'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('todo', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo',
            name='access_type',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Read only'), (2, 'Read and comment')], default=1),
        ),
        migrations.AlterUniqueTogether(
            name='todo',
            unique_together={('user', 'task')},
        ),
    ]