from django.contrib import admin
from django.core.exceptions import FieldDoesNotExist, ImproperlyConfigured
from django.db import models
from django.test import TestCase

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


class AdminAnchorTestCase(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.player_admin = PlayerAdmin(Player, admin.site)
        self.profile_admin = ProfileAdmin(Profile, admin.site)
        self.team_admin = TeamAdmin(Team, admin.site)

    def test_respects_the_model_admins_empty_value_display(self):
        player = Player.objects.create(name="John")

        class PlayerAdmin(admin.ModelAdmin):
            empty_value_display = "EMPTY"

            @admin_anchor("profile")
            def profile_link(self, instance):
                return "Profile"

        model_admin = PlayerAdmin(Player, admin.site)
        self.assertEqual(model_admin.profile_link(player), "EMPTY")

    def test_non_relation_field_cannot_be_referenced(self):
        player = Player.objects.create(name="John")
        self.assertRaises(ImproperlyConfigured, name_anchor, None, player)

    def test_raises_for_invalid_direct_field(self):
        player = Player.objects.create(name="John")
        self.assertRaises(FieldDoesNotExist, invalid_direct_field_anchor, None, player)

    def test_raises_for_invalid_indirect_field(self):
        player = Player.objects.create(name="John")
        team = Team.objects.create(captain=player)
        self.assertRaises(FieldDoesNotExist, invalid_indirect_field_anchor, None, team)

    def test_empty_direct_obj_results_in_empty_anchor(self):
        self.assertEqual(profile_anchor(self.profile_admin, None), "-")

    def test_empty_indirect_obj_results_in_empty_anchor(self):
        team = Team.objects.create()
        self.assertIsNone(team.captain)
        self.assertEqual(captains_profile_anchor(self.profile_admin, team), "-")

    def test_one_to_one_rel_anchor_generation(self):
        player = Player.objects.create(name="John")
        profile = Profile.objects.create(player=player)
        self.assertIsInstance(player._meta.get_field("profile"), models.OneToOneRel)
        self.assertIsNotNone(player.profile)
        self.assertEqual(
            profile_anchor(None, player),
            f"<a href='/admin/gaming/profile/{profile.id}/change/'>Profile</a>",
        )

    def test_empty_one_to_one_rel_anchor_generation(self):
        player = Player.objects.create(name="John")
        self.assertIsInstance(player._meta.get_field("profile"), models.OneToOneRel)
        self.assertFalse(hasattr(player, "profile"))
        self.assertEqual(
            profile_anchor(self.profile_admin, player),
            "-",
        )

    def test_one_to_one_field_anchor_generation(self):
        player = Player.objects.create(name="John")
        profile = Profile.objects.create(player=player)
        self.assertIsInstance(profile._meta.get_field("player"), models.OneToOneField)
        self.assertIsNotNone(profile.player)
        self.assertEqual(
            player_anchor(self.profile_admin, profile),
            f"<a href='/admin/gaming/player/{player.id}/change/'>Player</a>",
        )

    def test_emtpy_one_to_one_field_anchor_generation(self):
        profile = Profile.objects.create()
        self.assertIsInstance(profile._meta.get_field("player"), models.OneToOneField)
        self.assertIsNone(profile.player)
        self.assertEqual(player_anchor(self.profile_admin, profile), "-")

    def test_foreign_key_anchor_generation(self):
        player = Player.objects.create(name="John")
        team = Team.objects.create(captain=player)
        self.assertIsInstance(team._meta.get_field("captain"), models.ForeignKey)
        self.assertIsNotNone(team.captain)
        self.assertEqual(
            captain_anchor(None, team),
            f"<a href='/admin/gaming/player/{player.id}/change/'>Captain</a>",
        )

    def test_empty_foreign_key_anchor_generation(self):
        team = Team.objects.create()
        self.assertIsInstance(team._meta.get_field("captain"), models.ForeignKey)
        self.assertIsNone(team.captain)
        self.assertEqual(captain_anchor(self.team_admin, team), "-")

    def test_many_to_one_rel_anchor_generation(self):
        player = Player.objects.create(name="John")
        team = Team.objects.create(captain=player)
        self.assertIsInstance(player._meta.get_field("led_teams"), models.ManyToOneRel)
        self.assertCountEqual(list(player.led_teams.all()), [team])
        self.assertEqual(
            led_teams_anchor(None, player),
            f"<a href='/admin/gaming/team/?captain__id={player.id}'>Led teams</a>",
        )

    def test_empty_many_to_one_rel_anchor_generation(self):
        player = Player.objects.create(name="John")
        self.assertIsInstance(player._meta.get_field("led_teams"), models.ManyToOneRel)
        self.assertCountEqual(list(player.led_teams.all()), [])
        self.assertEqual(
            led_teams_anchor(None, player),
            f"<a href='/admin/gaming/team/?captain__id={player.id}'>Led teams</a>",
        )

    def test_many_to_many_rel_anchor_generation(self):
        player = Player.objects.create(name="John")
        team = Team.objects.create()
        team.members.add(player)
        self.assertIsInstance(player._meta.get_field("teams"), models.ManyToManyRel)
        self.assertListEqual(list(player.teams.all()), [team])
        self.assertEqual(
            teams_anchor(None, player),
            f"<a href='/admin/gaming/team/?members__id={player.id}'>Teams</a>",
        )

    def test_empty_many_to_many_rel_anchor_generation(self):
        player = Player.objects.create(name="John")
        self.assertIsInstance(player._meta.get_field("teams"), models.ManyToManyRel)
        self.assertListEqual(list(player.teams.all()), [])
        self.assertEqual(
            teams_anchor(None, player),
            f"<a href='/admin/gaming/team/?members__id={player.id}'>Teams</a>",
        )

    def test_many_to_many_field_anchor_generation(self):
        player = Player.objects.create(name="John")
        team = Team.objects.create()
        team.members.add(player)
        self.assertIsInstance(team._meta.get_field("members"), models.ManyToManyField)
        self.assertListEqual(list(team.members.all()), [player])
        self.assertEqual(
            members_anchor(None, team),
            f"<a href='/admin/gaming/player/?teams__id={team.id}'>Members</a>",
        )

    def test_empty_many_to_many_field_anchor_generation(self):
        team = Team.objects.create()
        self.assertIsInstance(team._meta.get_field("members"), models.ManyToManyField)
        self.assertListEqual(list(team.members.all()), [])
        self.assertEqual(
            members_anchor(None, team),
            f"<a href='/admin/gaming/player/?teams__id={team.id}'>Members</a>",
        )

    def test_indirect_many_to_many_rel_field_anchor_generation(self):
        player = Player.objects.create(name="John")
        profile = Profile.objects.create(player=player)
        team = Team.objects.create()
        team.members.add(player)
        self.assertIsInstance(player._meta.get_field("teams"), models.ManyToManyRel)
        self.assertListEqual(list(player.teams.all()), [team])
        self.assertEqual(
            player_teams_anchor(None, profile),
            f"<a href='/admin/gaming/team/?members__id={player.id}'>Teams</a>",
        )

    def test_empty_indirect_many_to_many_rel_field_anchor_generation(self):
        player = Player.objects.create(name="John")
        profile = Profile.objects.create(player=player)
        self.assertIsInstance(player._meta.get_field("teams"), models.ManyToManyRel)
        self.assertListEqual(list(player.teams.all()), [])
        self.assertEqual(
            player_teams_anchor(None, profile),
            f"<a href='/admin/gaming/team/?members__id={player.id}'>Teams</a>",
        )

    def test_indirect_one_to_one_rel_field_anchor_generation(self):
        player = Player.objects.create(name="John")
        profile = Profile.objects.create(player=player)
        team = Team.objects.create(captain=player)
        self.assertIsInstance(
            team.captain._meta.get_field("profile"), models.OneToOneRel
        )
        self.assertIsNotNone(player.profile)
        self.assertEqual(
            captains_profile_anchor(None, team),
            f"<a href='/admin/gaming/profile/{profile.id}/change/'>Profile</a>",
        )

    def test_empty_indirect_one_to_one_rel_field_anchor_generation(self):
        player = Player.objects.create(name="John")
        team = Team.objects.create(captain=player)
        self.assertIsInstance(
            team.captain._meta.get_field("profile"), models.OneToOneRel
        )
        self.assertFalse(hasattr(player, "profile"))
        self.assertEqual(captains_profile_anchor(self.team_admin, team), "-")
