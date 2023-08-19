from django.db import models


class Registration(models.Model):
    id = models.AutoField(primary_key=True)
    hackathon = models.ForeignKey("hackathon.Hackathon", on_delete=models.CASCADE)
    user = models.ForeignKey("user.User", on_delete=models.CASCADE, null=True, blank=True)
    team = models.ForeignKey("team.Team", on_delete=models.CASCADE, null=True, blank=True)
    timestampRegistered = models.DateTimeField(auto_now_add=True)
    meta = models.JSONField(default=dict)

    class Meta:
        verbose_name = 'Registration'
        verbose_name_plural = 'Registrations'

    def __str__(self):
        return f"{self.user} - {self.hackathon}"


__all__ = [
    'Registration',
]
