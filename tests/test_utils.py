from django.core.exceptions import FieldDoesNotExist
from django.test import TestCase

from admin_anchors.utils import (
    create_admin_anchor,
    get_selected_field,
    get_selected_obj,
)
from tests.project.gaming.models import Player, Team


class GetSelectedObjTestCase(TestCase):
    def test_direct_related_object_selection(self):
        player = Player.objects.create(name="John")

        obj = get_selected_obj(player, "profile")
        self.assertEqual(obj, player)

    def test_indirect_related_object_selection(self):
        player = Player.objects.create(name="John")
        team = Team.objects.create(captain=player)

        obj = get_selected_obj(team, "captain.profile")
        self.assertEqual(obj, player)

    def test_invalid_selection_results_in_none(self):
        player = Player.objects.create(name="John")
        team = Team.objects.create(captain=player)

        obj = get_selected_obj(team, "NON_EXISTING_RELATION.profile")
        self.assertIsNone(obj)


class GetSelectedFieldTestCase(TestCase):
    def test_raises_if_direct_field_selection_is_invalid(self):
        player = Player.objects.create(name="John")

        with self.assertRaises(FieldDoesNotExist):
            get_selected_field(player, "NON_EXISTING_FIELD")

    def test_raises_if_indirect_field_selection_is_invalid(self):
        player = Player.objects.create(name="John")
        team = Team.objects.create(captain=player)

        with self.assertRaises(FieldDoesNotExist):
            get_selected_field(team, "captain.NON_EXISTING_FIELD")

    def test_returns_none_if_indirect_related_obj_selection_is_invalid(self):
        player = Player.objects.create(name="John")
        team = Team.objects.create(captain=player)

        field = get_selected_field(team, "NON_EXISTING_RELATION.profile")
        self.assertIsNone(field)


class CreateAdminAnchorTestCase(TestCase):
    def test_resolve_changelist_page(self):
        link = create_admin_anchor(
            page_name="changelist",
            app_label="gaming",
            model_name="player",
            label="Players",
        )
        expectation = "<a href='/admin/gaming/player/'>Players</a>"
        self.assertEqual(link, expectation)

    def test_resolve_filtered_changelist_page(self):
        link = create_admin_anchor(
            page_name="changelist",
            app_label="gaming",
            model_name="player",
            label="Players",
            query={"teams__id": 1},
        )
        expectation = "<a href='/admin/gaming/player/?teams__id=1'>Players</a>"
        self.assertEqual(link, expectation)

    def test_resolve_change_page(self):
        player = Player.objects.create(name="John")
        link = create_admin_anchor(
            page_name="change",
            app_label="gaming",
            model_name="player",
            label="Player",
            args=[player.pk],
        )
        expectation = f"<a href='/admin/gaming/player/{player.pk}/change/'>Player</a>"
        self.assertEqual(link, expectation)
