from django.db import models


class Hackathon(models.Model):
    SUBMISSION_TYPE = (
        ('image', 'Image'),
        ('file', 'File'),
        ('link', 'Link'),
    )

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    logo = models.ImageField(upload_to='hackathon/logo', null=True, blank=True)
    cover = models.ImageField(upload_to='hackathon/cover', null=True, blank=True)

    allowedSubmissionType = models.CharField(max_length=255, choices=SUBMISSION_TYPE, default='file')
    minimumTeamSize = models.IntegerField(default=0)
    maximumTeamSize = models.IntegerField(default=0)
    allowIndividual = models.BooleanField(default=False)

    startTimestamp = models.DateTimeField()
    endTimestamp = models.DateTimeField()
    pricePool = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Hackathon'
        verbose_name_plural = 'Hackathons'

    def __str__(self):
        return f"{self.title}"


__all__ = [
    'Hackathon',
]
