import pytest

from admin_anchors.utils import resolve_instance_field_path, create_admin_anchor
from tests.project.gaming.models import Player, Team, Profile


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
def test_resolving_path(team, profile):
    assert resolve_instance_field_path(team, ["captain", "profile"]) == profile


@pytest.mark.django_db
def test_resolving_nullable_relation(player):
    assert resolve_instance_field_path(player, ["profile"]) is None


@pytest.mark.django_db
def test_resolving_invalid_field(player):
    with pytest.raises(AttributeError):
        resolve_instance_field_path(player, ["NON_EXISTING_FIELD"])


@pytest.mark.django_db
def test_resolving_empty_path(player):
    assert resolve_instance_field_path(player, []) == player


def test_create_admin_anchor_resolves_changelist_page():
    link = create_admin_anchor(
        page_name="changelist",
        app_label="gaming",
        model_name="player",
        label="Players",
    )
    assert link == "<a href='/admin/gaming/player/'>Players</a>"


def test_create_admin_anchor_resolves_filtered_changelist_page():
    link = create_admin_anchor(
        page_name="changelist",
        app_label="gaming",
        model_name="player",
        label="Players",
        query={"teams__id": 1},
    )
    assert link == "<a href='/admin/gaming/player/?teams__id=1'>Players</a>"


@pytest.mark.django_db
def test_create_admin_anchor_resolves_change_page(player):
    link = create_admin_anchor(
        page_name="change",
        app_label="gaming",
        model_name="player",
        label="Player",
        args=[player.pk],
    )
    assert link == f"<a href='/admin/gaming/player/{player.pk}/change/'>Player</a>"
