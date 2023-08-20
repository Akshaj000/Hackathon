from django.db import models
from rest_framework.exceptions import ValidationError


class Registration(models.Model):
    id = models.AutoField(primary_key=True)
    hackathon = models.ForeignKey("hackathon.Hackathon", on_delete=models.CASCADE)
    user = models.ForeignKey("user.User", on_delete=models.CASCADE, null=True, blank=True)
    team = models.ForeignKey("team.Team", on_delete=models.CASCADE, null=True, blank=True)
    timestampRegistered = models.DateTimeField(auto_now_add=True)
    meta = models.JSONField(default=dict)

    def clean(self):
        allow_individual = self.hackathon.allowIndividual
        min_team_size = self.hackathon.minimumTeamSize
        max_team_size = self.hackathon.maximumTeamSize

        if not allow_individual:
            if not self.team:
                raise ValidationError("A team is required for registration in this hackathon.")
            if min_team_size < 1 or max_team_size < 1 or max_team_size < min_team_size:
                raise ValidationError("Invalid team size range.")

        elif allow_individual and self.team:
            raise ValidationError("Individuals cannot be part of a team for this hackathon.")

        elif not allow_individual and self.user and self.team.teammember_set.filter(user=self.user).count() == 0:
            raise ValidationError("The registered user must be a member of the team.")

    class Meta:
        verbose_name = 'Registration'
        verbose_name_plural = 'Registrations'
        unique_together = (('hackathon', 'team'), ('hackathon', 'user'))

    def __str__(self):
        return f"{self.user} - {self.hackathon}"


__all__ = [
    'Registration',
]
