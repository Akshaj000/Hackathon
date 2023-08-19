from django.db import models


class Submission(models.Model):
    id = models.AutoField(primary_key=True)
    hackathon = models.ForeignKey("hackathon.Hackathon", on_delete=models.CASCADE)
    user = models.ForeignKey("user.User", on_delete=models.CASCADE, null=True, blank=True)
    team = models.ForeignKey("team.Team", on_delete=models.CASCADE, null=True, blank=True)

    file = models.FileField(upload_to='hackathon/submission', null=True, blank=True)
    link = models.URLField(null=True, blank=True)

    summary = models.TextField(null=True, blank=True)
    timestampSubmitted = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Submission'
        verbose_name_plural = 'Submissions'

    def __str__(self):
        str(self.id)


__all__ = [
    'Submission',
]
