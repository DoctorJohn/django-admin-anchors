import pytest
from django.core.exceptions import FieldDoesNotExist

from admin_anchors.utils import (
    create_admin_anchor,
    get_selected_field,
    get_selected_obj,
)
from tests.project.gaming.models import Player, Team


@pytest.fixture
def player():
    return Player.objects.create(name="John")


@pytest.fixture
def team(player):
    return Team.objects.create(captain=player)


@pytest.mark.django_db
def test_get_selected_obj_direct_related_object_selection(player):
    obj = get_selected_obj(player, "profile")
    assert obj == player


@pytest.mark.django_db
def test_get_selected_obj_indirect_related_object_selection(player, team):
    obj = get_selected_obj(team, "captain.profile")
    assert obj == player


@pytest.mark.django_db
def test_get_selected_obj_invalid_selection_results_in_none(team):
    obj = get_selected_obj(team, "NON_EXISTING_RELATION.profile")
    assert obj is None


@pytest.mark.django_db
def test_get_selected_field_raises_if_direct_field_selection_is_invalid(player):
    with pytest.raises(FieldDoesNotExist):
        get_selected_field(player, "NON_EXISTING_FIELD")


@pytest.mark.django_db
def test_get_selected_field_raises_if_indirect_field_selection_is_invalid(team):
    with pytest.raises(FieldDoesNotExist):
        get_selected_field(team, "captain.NON_EXISTING_FIELD")


@pytest.mark.django_db
def test_get_delected_field_returns_none_if_indirect_related_obj_selection_is_invalid(
    team,
):
    field = get_selected_field(team, "NON_EXISTING_RELATION.profile")
    assert field is None


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
