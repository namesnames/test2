# Generated by Django 4.0.6 on 2022-07-26 07:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_category_user_category_list'),
        ('profiles', '0003_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pop',
            name='foregin_category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.category'),
        ),
        migrations.DeleteModel(
            name='Category',
        ),
    ]
