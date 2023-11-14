import pytest
from django.contrib import admin
from django.core.exceptions import FieldDoesNotExist, ImproperlyConfigured
from django.db import models

from admin_anchors import admin_anchor
from tests.project.gaming.admin import PlayerAdmin, ProfileAdmin, TeamAdmin
from tests.project.gaming.models import Player, Profile, Team


@admin_anchor("name")
def name_anchor(self, instance):
    return "Name"


@admin_anchor("NON_EXISTING_FIELD")
def invalid_direct_field_anchor(self, instance):
    return "Invalid"


@admin_anchor("captain.NON_EXISTING_FIELD")
def invalid_indirect_field_anchor(self, instance):
    return "Invalid"


@admin_anchor("profile")
def profile_anchor(self, instance):
    return "Profile"


@admin_anchor("captain.profile")
def captains_profile_anchor(self, instance):
    return "Profile"


@admin_anchor("player")
def player_anchor(self, instance):
    return "Player"


@admin_anchor("captain")
def captain_anchor(self, instance):
    return "Captain"


@admin_anchor("led_teams")
def led_teams_anchor(self, instance):
    return "Led teams"


@admin_anchor("teams")
def teams_anchor(self, instance):
    return "Teams"


@admin_anchor("members")
def members_anchor(self, instance):
    return "Members"


@admin_anchor("player.teams")
def player_teams_anchor(self, instance):
    return "Teams"


@pytest.fixture
def player_admin():
    return PlayerAdmin(Player, admin.site)


@pytest.fixture
def profile_admin():
    return ProfileAdmin(Profile, admin.site)


@pytest.fixture
def team_admin():
    return TeamAdmin(Team, admin.site)


@pytest.fixture
def player():
    return Player.objects.create(name="John")


@pytest.fixture
def profile(player):
    return Profile.objects.create(player=player)


@pytest.fixture
def team(player):
    return Team.objects.create(captain=player)


@pytest.mark.django_db
def test_respects_the_model_admins_empty_value_display(player):
    class PlayerAdmin(admin.ModelAdmin):
        empty_value_display = "EMPTY"

        @admin_anchor("profile")
        def profile_link(self, instance):
            return "Profile"

    model_admin = PlayerAdmin(Player, admin.site)
    assert model_admin.profile_link(player) == "EMPTY"


@pytest.mark.django_db
def test_non_relation_field_cannot_be_referenced(player):
    with pytest.raises(ImproperlyConfigured):
        name_anchor(None, player)


@pytest.mark.django_db
def test_raises_for_invalid_direct_field(player):
    with pytest.raises(FieldDoesNotExist):
        invalid_direct_field_anchor(None, player)


@pytest.mark.django_db
def test_raises_for_invalid_indirect_field(team):
    with pytest.raises(FieldDoesNotExist):
        invalid_indirect_field_anchor(None, team)


def test_empty_direct_obj_results_in_empty_anchor(profile_admin):
    assert profile_anchor(profile_admin, None) == "-"


@pytest.mark.django_db
def test_empty_indirect_obj_results_in_empty_anchor(profile_admin):
    team = Team.objects.create()

    assert team.captain is None
    assert captains_profile_anchor(profile_admin, team) == "-"


@pytest.mark.django_db
def test_one_to_one_rel_anchor_generation(player, profile):
    assert isinstance(player._meta.get_field("profile"), models.OneToOneRel)
    assert player.profile is not None
    assert profile_anchor(None, player) == f"<a href='/admin/gaming/profile/?pk={profile.pk}'>Profile</a>"


@pytest.mark.django_db
def test_empty_one_to_one_rel_anchor_generation(player, profile_admin):
    assert isinstance(player._meta.get_field("profile"), models.OneToOneRel)
    assert not hasattr(player, "profile")
    assert profile_anchor(profile_admin, player) == "-"


@pytest.mark.django_db
def test_one_to_one_field_anchor_generation(player, profile, profile_admin):
    assert isinstance(profile._meta.get_field("player"), models.OneToOneField)
    assert profile.player is not None
    assert player_anchor(profile_admin, profile) == f"<a href='/admin/gaming/player/?pk={player.pk}'>Player</a>"


@pytest.mark.django_db
def test_emtpy_one_to_one_field_anchor_generation(profile_admin):
    profile = Profile.objects.create()

    assert isinstance(profile._meta.get_field("player"), models.OneToOneField)
    assert profile.player is None
    assert player_anchor(profile_admin, profile) == "-"


@pytest.mark.django_db
def test_foreign_key_anchor_generation(player, team):
    assert isinstance(team._meta.get_field("captain"), models.ForeignKey)
    assert team.captain is not None
    assert captain_anchor(None, team) == f"<a href='/admin/gaming/player/?pk={player.pk}'>Captain</a>"


@pytest.mark.django_db
def test_empty_foreign_key_anchor_generation(team_admin):
    team = Team.objects.create()

    assert isinstance(team._meta.get_field("captain"), models.ForeignKey)
    assert team.captain is None
    assert captain_anchor(team_admin, team) == "-"


@pytest.mark.django_db
def test_many_to_one_rel_anchor_generation(player, team):
    assert isinstance(player._meta.get_field("led_teams"), models.ManyToOneRel)
    assert list(player.led_teams.all()) == [team]
    assert led_teams_anchor(None, player) == f"<a href='/admin/gaming/team/?captain__pk={player.pk}'>Led teams</a>"


@pytest.mark.django_db
def test_empty_many_to_one_rel_anchor_generation(player):
    assert isinstance(player._meta.get_field("led_teams"), models.ManyToOneRel)
    assert list(player.led_teams.all()) == []
    assert led_teams_anchor(None, player) == f"<a href='/admin/gaming/team/?captain__pk={player.pk}'>Led teams</a>"


@pytest.mark.django_db
def test_many_to_many_rel_anchor_generation(player, team):
    team.members.add(player)

    assert isinstance(player._meta.get_field("teams"), models.ManyToManyRel)
    assert list(player.teams.all()) == [team]
    assert teams_anchor(None, player) == f"<a href='/admin/gaming/team/?members__pk={player.pk}'>Teams</a>"


@pytest.mark.django_db
def test_empty_many_to_many_rel_anchor_generation(player):
    assert isinstance(player._meta.get_field("teams"), models.ManyToManyRel)
    assert list(player.teams.all()) == []
    assert teams_anchor(None, player) == f"<a href='/admin/gaming/team/?members__pk={player.pk}'>Teams</a>"


@pytest.mark.django_db
def test_many_to_many_field_anchor_generation(player, team):
    team.members.add(player)

    assert isinstance(team._meta.get_field("members"), models.ManyToManyField)
    assert list(team.members.all()) == [player]
    assert members_anchor(None, team) == f"<a href='/admin/gaming/player/?teams__pk={team.pk}'>Members</a>"


@pytest.mark.django_db
def test_empty_many_to_many_field_anchor_generation(team):
    assert isinstance(team._meta.get_field("members"), models.ManyToManyField)
    assert list(team.members.all()) == []
    assert members_anchor(None, team) == f"<a href='/admin/gaming/player/?teams__pk={team.pk}'>Members</a>"


@pytest.mark.django_db
def test_indirect_many_to_many_rel_field_anchor_generation(player, profile, team):
    team.members.add(player)

    assert isinstance(player._meta.get_field("teams"), models.ManyToManyRel)
    assert list(player.teams.all()) == [team]
    assert player_teams_anchor(None, profile) == f"<a href='/admin/gaming/team/?members__pk={player.pk}'>Teams</a>"


@pytest.mark.django_db
def test_empty_indirect_many_to_many_rel_field_anchor_generation(player, profile):
    assert isinstance(player._meta.get_field("teams"), models.ManyToManyRel)
    assert list(player.teams.all()) == []
    assert player_teams_anchor(None, profile) == f"<a href='/admin/gaming/team/?members__pk={player.pk}'>Teams</a>"


@pytest.mark.django_db
def test_indirect_one_to_one_rel_field_anchor_generation(player, profile, team):
    assert isinstance(team.captain._meta.get_field("profile"), models.OneToOneRel)
    assert player.profile is not None
    assert captains_profile_anchor(None, team) == f"<a href='/admin/gaming/profile/?pk={profile.pk}'>Profile</a>"


@pytest.mark.django_db
def test_empty_indirect_one_to_one_rel_field_anchor_generation(player, team, team_admin):
    assert isinstance(team.captain._meta.get_field("profile"), models.OneToOneRel)
    assert not hasattr(player, "profile")
    assert captains_profile_anchor(team_admin, team) == "-"
