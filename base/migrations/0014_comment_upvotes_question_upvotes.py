# Generated by Django 4.2.5 on 2023-09-28 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0013_remove_comment_parent_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='upvotes',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='question',
            name='upvotes',
            field=models.PositiveIntegerField(default=0),
        ),
    ]