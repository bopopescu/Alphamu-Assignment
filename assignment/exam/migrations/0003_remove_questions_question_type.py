# Generated by Django 2.2.6 on 2019-10-29 09:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0002_remove_answers_answer_score'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='questions',
            name='question_type',
        ),
    ]