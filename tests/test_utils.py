import pytest
from django.core.exceptions import FieldDoesNotExist

from admin_anchors.utils import (
    create_admin_anchor,
    get_selected_field,
    get_selected_obj,
)
from tests.project.gaming.models import Player, Team


@pytest.mark.django_db
def test_get_selected_obj_direct_related_object_selection():
    player = Player.objects.create(name="John")

    obj = get_selected_obj(player, "profile")
    assert obj == player


@pytest.mark.django_db
def test_get_selected_obj_indirect_related_object_selection():
    player = Player.objects.create(name="John")
    team = Team.objects.create(captain=player)

    obj = get_selected_obj(team, "captain.profile")
    assert obj == player


@pytest.mark.django_db
def test_get_selected_obj_invalid_selection_results_in_none():
    player = Player.objects.create(name="John")
    team = Team.objects.create(captain=player)

    obj = get_selected_obj(team, "NON_EXISTING_RELATION.profile")
    assert obj is None


@pytest.mark.django_db
def test_get_selected_field_raises_if_direct_field_selection_is_invalid():
    player = Player.objects.create(name="John")

    with pytest.raises(FieldDoesNotExist):
        get_selected_field(player, "NON_EXISTING_FIELD")


@pytest.mark.django_db
def test_get_selected_field_raises_if_indirect_field_selection_is_invalid():
    player = Player.objects.create(name="John")
    team = Team.objects.create(captain=player)

    with pytest.raises(FieldDoesNotExist):
        get_selected_field(team, "captain.NON_EXISTING_FIELD")


@pytest.mark.django_db
def test_get_delected_field_returns_none_if_indirect_related_obj_selection_is_invalid():
    player = Player.objects.create(name="John")
    team = Team.objects.create(captain=player)

    field = get_selected_field(team, "NON_EXISTING_RELATION.profile")
    assert field is None


def test_create_admin_anchor_resolves_changelist_page():
    link = create_admin_anchor(
        page_name="changelist",
        app_label="gaming",
        model_name="player",
        label="Players",
    )
    expectation = "<a href='/admin/gaming/player/'>Players</a>"
    assert link == expectation


def test_create_admin_anchor_resolves_filtered_changelist_page():
    link = create_admin_anchor(
        page_name="changelist",
        app_label="gaming",
        model_name="player",
        label="Players",
        query={"teams__id": 1},
    )
    expectation = "<a href='/admin/gaming/player/?teams__id=1'>Players</a>"
    assert link == expectation


@pytest.mark.django_db
def test_create_admin_anchor_resolves_change_page():
    player = Player.objects.create(name="John")
    link = create_admin_anchor(
        page_name="change",
        app_label="gaming",
        model_name="player",
        label="Player",
        args=[player.pk],
    )
    expectation = f"<a href='/admin/gaming/player/{player.pk}/change/'>Player</a>"
    assert link == expectation
