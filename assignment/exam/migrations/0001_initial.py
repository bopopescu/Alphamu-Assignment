# Generated by Django 2.2.6 on 2019-10-29 08:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Answers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer_text', models.TextField(blank=True, max_length=200, null=True)),
                ('answer_score', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'answers',
            },
        ),
        migrations.CreateModel(
            name='Questions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.TextField(blank=True, max_length=200, null=True)),
                ('question_type', models.CharField(blank=True, choices=[('Text', 'Text'), ('Short', 'Short'), ('Essay', 'Essay'), ('Multiple Choice', 'Multiple Choice'), ('Matching', 'Matching')], default='', max_length=50, null=True)),
                ('answer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='question_answer', to='exam.Answers')),
            ],
            options={
                'db_table': 'questions',
            },
        ),
    ]
