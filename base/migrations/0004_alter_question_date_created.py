# Generated by Django 4.2.5 on 2023-09-24 05:24

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_question_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='date_created',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
