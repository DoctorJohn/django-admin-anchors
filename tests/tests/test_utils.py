from django.test import TestCase
from admin_anchors.utils import create_admin_anchor
from tests.project.gaming.models import Player


class UtilsTestCase(TestCase):
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
