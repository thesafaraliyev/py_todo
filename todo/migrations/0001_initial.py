# Generated by Django 3.0.5 on 2020-04-24 20:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('task', '0002_auto_20200424_2345'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Todo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('access_type', models.PositiveSmallIntegerField(choices=[(1, 'read'), (2, 'read and comment')], default=1)),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='task.Task')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
