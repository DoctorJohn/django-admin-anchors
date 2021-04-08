from django.contrib import admin
from admin_anchors import admin_anchor
from tests.project.gaming.models import Player, Profile, Team


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ["__str__", "profile_link", "teams_link", "led_teams_link"]

    @admin_anchor(field_name="profile")
    def profile_link(self, instance):
        return "Profile"

    @admin_anchor(field_name="teams")
    def teams_link(self, instance):
        return f"{instance.teams.count()} teams"

    @admin_anchor(field_name="led_teams")
    def led_teams_link(self, instance):
        return f"{instance.led_teams.count()} led teams"


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["__str__", "player_link", "player_teams_link"]

    @admin_anchor(field_name="player")
    def player_link(self, instance):
        return str(instance.player)

    @admin_anchor(field_name="player.teams")
    def player_teams_link(self, instance):
        return f"{instance.player.teams.count()} teams"


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ["__str__", "captain_link", "captains_profile_link", "members_link"]

    @admin_anchor(field_name="captain")
    def captain_link(self, instance):
        return str(instance.captain)

    @admin_anchor(field_name="captain.profile")
    def captains_profile_link(self, instance):
        return "Captains profile"

    @admin_anchor(field_name="members")
    def members_link(self, instance):
        return f"{instance.members.count()} members"
