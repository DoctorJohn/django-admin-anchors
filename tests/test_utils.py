import pytest

from admin_anchors.utils import create_admin_anchor, resolve_instance_field_path
from tests.project.gaming.models import Player, Profile, Team


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


def test_create_admin_anchor():
    link = create_admin_anchor(
        app_label="gaming",
        model_name="player",
        label="Players",
        query={"teams__id": 1},
    )
    assert link == "<a href='/admin/gaming/player/?teams__id=1'>Players</a>"
