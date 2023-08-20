from django.db import models


class Evaluation(models.Model):
    id = models.AutoField(primary_key=True)
    submission = models.OneToOneField("hackathon.Submission", on_delete=models.CASCADE)
    evaluator = models.ForeignKey("hackathon.Organiser", on_delete=models.CASCADE)

    review = models.TextField(null=True, blank=True)
    score = models.IntegerField(default=0)

    timestampEvaluated = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Evaluation'
        verbose_name_plural = 'Evaluations'

    def __str__(self):
        return f"{self.submission} - {self.evaluator}"


__all__ = [
    'Evaluation',
]
