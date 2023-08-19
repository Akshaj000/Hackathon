from django.db import models


class TeamMember(models.Model):
    user = models.ForeignKey("user.User", on_delete=models.CASCADE)
    team = models.ForeignKey("team.Team", on_delete=models.CASCADE)
    isOwner = models.BooleanField(default=False)
    meta = models.JSONField(default=dict)

    class Meta:
        verbose_name = 'Team Member'
        verbose_name_plural = 'Team Members'

    def __str__(self):
        return f"{self.user} - {self.team}"


__all__ = [
    'TeamMember',
]
