# Generated by Django 4.2.5 on 2023-09-28 14:06

from django.db import migrations, models
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0021_remove_question_contents_alter_question_content'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='contents',
            field=tinymce.models.HTMLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='content',
            field=models.TextField(blank=True, null=True),
        ),
    ]