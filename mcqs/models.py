from django.db import models


class MCQQuestion(models.Model):
    question_text = models.CharField(max_length=300)
    pub_date = models.DateTimeField("date published")

    class Meta:
        verbose_name = "MCQ Question"
        verbose_name_plural = "MCQ Questions"
        ordering = ["-pub_date"]

    def __str__(self):
        return self.question_text


class MCQOption(models.Model):
    question = models.ForeignKey(MCQQuestion, on_delete=models.CASCADE)
    option_text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

    class Meta:
        verbose_name = "MCQ Option"
        verbose_name_plural = "MCQ Options"

    def __str__(self):
        return self.option_text
