# Generated by Django 4.2.5 on 2023-09-28 12:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0018_remove_comment_downvotes_remove_comment_upvotes_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='comment_count',
        ),
    ]
