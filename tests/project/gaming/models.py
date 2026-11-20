from django.db import models


class Player(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class Profile(models.Model):
    player = models.OneToOneField(
        Player, on_delete=models.CASCADE, related_name="profile", blank=True, null=True
    )

    def __str__(self):
        return f"Profile of {self.player}"


class Team(models.Model):
    name = models.CharField(max_length=32)

    members = models.ManyToManyField(Player, related_name="teams")

    captain = models.ForeignKey(
        Player,
        on_delete=models.CASCADE,
        related_name="led_teams",
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.name


class Tournament(models.Model):
    name = models.CharField(max_length=32)

    # Neither relation sets a related_name, so their reverse accessors use
    # Django's defaults (player.tournament_set and team.tournament_set),
    # which differ from their related query names ("tournament").
    participants = models.ManyToManyField(Team)

    host = models.ForeignKey(
        Player,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.name
