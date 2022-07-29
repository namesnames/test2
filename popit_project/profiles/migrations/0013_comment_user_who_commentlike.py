# Generated by Django 4.0.6 on 2022-07-29 17:30

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('profiles', '0012_pop_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='user_who_commentlike',
            field=models.ManyToManyField(blank=True, related_name='user_who_commentlike', to=settings.AUTH_USER_MODEL),
        ),
    ]
