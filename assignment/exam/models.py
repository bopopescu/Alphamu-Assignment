from django.db import models


# Create your models here.
class Answers(models.Model):
    answer_text = models.TextField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.answer_text

    class Meta:
        db_table = "answers"


class Questions(models.Model):
    answer = models.ForeignKey(Answers, related_name='question_answer', null=True, on_delete=models.CASCADE)
    question_text = models.TextField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.question_text

    class Meta:
        db_table = "questions"
