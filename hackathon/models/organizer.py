from django.db import models


class Organiser(models.Model):
    ACCESS_TYPE = (
        (0, 'admin'),
        (1, 'editor'),
        (2, 'viewer'),
    )

    user = models.ForeignKey("user.User", on_delete=models.CASCADE)
    hackathon = models.ForeignKey("hackathon.Hackathon", on_delete=models.CASCADE)
    access = models.IntegerField(choices=ACCESS_TYPE, default=2)

    class Meta:
        verbose_name = 'Organiser'
        verbose_name_plural = 'Organisers'
        unique_together = (('user', 'hackathon'),)

    def __str__(self):
        return self.user.username


__all__ = [
    'Organiser',
]
