# Generated by Django 4.2.5 on 2023-09-28 10:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0012_comment_parent_comment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='parent_comment',
        ),
    ]
