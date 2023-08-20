from django.db import models
from rest_framework.exceptions import ValidationError


class Submission(models.Model):
    id = models.AutoField(primary_key=True)
    hackathon = models.ForeignKey("hackathon.Hackathon", on_delete=models.CASCADE)
    user = models.ForeignKey("user.User", on_delete=models.CASCADE, null=True, blank=True)
    team = models.ForeignKey("team.Team", on_delete=models.CASCADE, null=True, blank=True)

    image = models.ImageField(upload_to='hackathon/submission', null=True, blank=True)
    file = models.FileField(upload_to='hackathon/submission', null=True, blank=True)
    link = models.URLField(null=True, blank=True)

    summary = models.TextField(null=True, blank=True)
    timestampSubmitted = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if not self.file and not self.image and not self.link:
            raise ValidationError("At least one of file, image, or link must be provided.")
        if sum(1 for field in [self.file, self.image, self.link] if field) > 1:
            raise ValidationError("Only one of file, image, or link should be provided.")

        allowed_type = self.hackathon.allowedSubmissionType

        if self.image and allowed_type != 'image':
            raise ValidationError("Submitted content type is not allowed for this hackathon.")
        if self.file and allowed_type != 'file':
            raise ValidationError("Submitted content type is not allowed for this hackathon.")
        if self.link and allowed_type != 'link':
            raise ValidationError("Submitted content type is not allowed for this hackathon.")

    class Meta:
        verbose_name = 'Submission'
        verbose_name_plural = 'Submissions'
        unique_together = (('hackathon', 'team'), ('hackathon', 'user'))

    def __str__(self):
        return str(self.id)


__all__ = [
    'Submission',
]
