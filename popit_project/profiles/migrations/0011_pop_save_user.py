# Generated by Django 4.0.6 on 2022-07-27 12:08

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('profiles', '0010_alter_pop_user_who_like'),
    ]

    operations = [
        migrations.AddField(
            model_name='pop',
            name='save_user',
            field=models.ManyToManyField(blank=True, related_name='save_pop', to=settings.AUTH_USER_MODEL),
        ),
    ]
