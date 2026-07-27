from django.conf import settings
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


class MCQAnswer(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    question = models.ForeignKey(MCQQuestion, on_delete=models.CASCADE)
    selected_option = models.ForeignKey(MCQOption, on_delete=models.CASCADE)
    is_correct = models.BooleanField()
    answered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "question")
        ordering = ["-answered_at"]

    def __str__(self):
        return f"{self.user.username} - {self.question.question_text[:30]}"
