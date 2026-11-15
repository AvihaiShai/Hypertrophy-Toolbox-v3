"""Characterization coverage for the WP1.4 superset service boundary."""
import logging
import re
import subprocess
import sys
import time

import pytest


@pytest.mark.parametrize(
    "imports",
    [
        "import routes.workout_plan; import utils.supersets",
        "import utils.supersets; import routes.workout_plan",
    ],
)
def test_superset_modules_import_in_either_order(imports):
    completed = subprocess.run(
        [sys.executable, "-c", imports],
        capture_output=True,
        text=True,
        check=False,
    )

    assert completed.returncode == 0, completed.stderr


def test_route_helper_imports_remain_compatible():
    from routes import workout_plan
    from utils import supersets

    assert (
        workout_plan._validate_superset_link_request
        is supersets._validate_superset_link_request
    )
    assert workout_plan._apply_superset_link is supersets._apply_superset_link
    assert (
        workout_plan._group_exercises_by_routine
        is supersets._group_exercises_by_routine
    )
    assert (
        workout_plan._find_antagonist_pairings
        is supersets._find_antagonist_pairings
    )
    assert (
        workout_plan.unlink_partner_for_removal
        is supersets.unlink_partner_for_removal
    )


def _link_pair(clean_db, workout_plan_factory, exercise_factory, group):
    first = exercise_factory("Removal First")
    second = exercise_factory("Removal Second")
    first_id = workout_plan_factory(exercise_name=first, routine="R")
    second_id = workout_plan_factory(exercise_name=second, routine="R")
    clean_db.execute_query(
        "UPDATE user_selection SET superset_group = ? WHERE id IN (?, ?)",
        (group, first_id, second_id),
    )
    return first_id, second_id


def test_unlink_partner_for_removal_nulls_only_the_partner(
    clean_db, workout_plan_factory, exercise_factory
):
    """Partner is nulled; the removed row keeps its group (id != ? guard)."""
    from utils.database import DatabaseHandler
    from utils.supersets import unlink_partner_for_removal

    removed_id, partner_id = _link_pair(
        clean_db, workout_plan_factory, exercise_factory, "SS-R-1"
    )

    with DatabaseHandler() as db:
        # Raw string id characterizes the route's permissive int() coercion.
        unlink_partner_for_removal(db, str(removed_id), "SS-R-1")

    partner = clean_db.fetch_one(
        "SELECT superset_group FROM user_selection WHERE id = ?", (partner_id,)
    )
    removed = clean_db.fetch_one(
        "SELECT superset_group FROM user_selection WHERE id = ?", (removed_id,)
    )
    assert partner["superset_group"] is None
    assert removed["superset_group"] == "SS-R-1"


def test_unlink_partner_for_removal_uses_passed_handler(
    clean_db, workout_plan_factory, exercise_factory
):
    """The write flows through the caller's handler and auto-commits there.

    ``remove_exercise`` runs partner-unlink, log-delete, and exercise-delete
    in one ``DatabaseHandler``; each ``execute_query`` commits (commit=True).
    A separate connection therefore sees the null before the block exits.
    """
    from utils.database import DatabaseHandler
    from utils.supersets import unlink_partner_for_removal

    removed_id, partner_id = _link_pair(
        clean_db, workout_plan_factory, exercise_factory, "SS-R-2"
    )

    with DatabaseHandler() as db:
        unlink_partner_for_removal(db, removed_id, "SS-R-2")
        # Still inside the caller's context: a distinct handler already sees it.
        early = clean_db.fetch_one(
            "SELECT superset_group FROM user_selection WHERE id = ?",
            (partner_id,),
        )
        assert early["superset_group"] is None


def test_unlink_partner_for_removal_logs_removal(
    clean_db, workout_plan_factory, exercise_factory, caplog
):
    """Preserve the removal log message and the raw removed_exercise_id."""
    from utils.database import DatabaseHandler
    from utils.supersets import unlink_partner_for_removal

    removed_id, _partner_id = _link_pair(
        clean_db, workout_plan_factory, exercise_factory, "SS-R-3"
    )

    with caplog.at_level(logging.INFO, logger="hypertrophy_toolbox"):
        with DatabaseHandler() as db:
            unlink_partner_for_removal(db, str(removed_id), "SS-R-3")

    record = next(
        rec
        for rec in caplog.records
        if rec.message == "Unlinked partner exercise from superset due to removal"
    )
    assert record.superset_group == "SS-R-3"
    # Raw value is logged unchanged, not the int()-coerced SQL param.
    assert record.removed_exercise_id == str(removed_id)


def test_link_preserves_timestamp_id_and_database_row_order(
    client,
    exercise_factory,
    workout_plan_factory,
    monkeypatch,
):
    first = exercise_factory("First Exercise")
    second = exercise_factory("Second Exercise")
    first_id = workout_plan_factory(exercise_name=first, routine="A")
    second_id = workout_plan_factory(exercise_name=second, routine="A")
    monkeypatch.setattr(time, "time", lambda: 1_700_000_000.9)

    response = client.post(
        "/api/superset/link",
        # Reversed input characterizes the historical unordered SQL result.
        json={"exercise_ids": [str(second_id), float(first_id)]},
    )

    assert response.status_code == 200
    payload = response.get_json()
    assert re.fullmatch(
        r"SS-A-1700000000-[0-9a-f]{12}", payload['data']['superset_group']
    )
    assert [row['id'] for row in payload['data']['exercises']] == [
        first_id,
        second_id,
    ]
    assert payload['message'] == (
        "Linked 'First Exercise' and 'Second Exercise' as superset"
    )


def test_unlink_invalid_truthy_exercise_id_keeps_generic_500(client):
    """The endpoint historically lets int() failure reach its generic catch."""
    response = client.post(
        "/api/superset/unlink", json={"exercise_id": "not-an-integer"}
    )

    assert response.status_code == 500
    payload = response.get_json()
    assert payload['error']['code'] == "INTERNAL_ERROR"
    assert payload['error']['message'] == "Failed to unlink superset"


def _same_second_pairs(
    client, clean_db, exercise_factory, workout_plan_factory, monkeypatch,
    *, legacy=False,
):
    monkeypatch.setattr(time, "time", lambda: 1_700_000_000.9)
    ids = [
        workout_plan_factory(
            exercise_name=exercise_factory(f"Same-second exercise {index}"),
            routine="A",
        )
        for index in range(4)
    ]
    if legacy:
        first_group = "SS-A-1700000000"
        clean_db.execute_query(
            "UPDATE user_selection SET superset_group = ? WHERE id IN (?, ?)",
            (first_group, *ids[:2]),
        )
    else:
        first = client.post("/api/superset/link", json={"exercise_ids": ids[:2]})
        assert first.status_code == 200
        first_group = first.get_json()["data"]["superset_group"]
    second = client.post("/api/superset/link", json={"exercise_ids": ids[2:]})
    assert second.status_code == 200
    return ids, first_group, second.get_json()["data"]["superset_group"]


def test_disjoint_supersets_created_in_the_same_second_stay_separate(
    client, clean_db, exercise_factory, workout_plan_factory, monkeypatch,
):
    ids, first_group, second_group = _same_second_pairs(
        client, clean_db, exercise_factory, workout_plan_factory, monkeypatch,
    )
    assert first_group != second_group
    rows = clean_db.fetch_all(
        "SELECT id, superset_group FROM user_selection ORDER BY id"
    )
    assert {row["id"]: row["superset_group"] for row in rows} == {
        ids[0]: first_group, ids[1]: first_group,
        ids[2]: second_group, ids[3]: second_group,
    }


@pytest.mark.parametrize("legacy", [False, True], ids=["new-pairs", "legacy-pair"])
@pytest.mark.parametrize("operation", ["unlink", "remove"])
@pytest.mark.parametrize("pair_index", [0, 1], ids=["first-pair", "second-pair"])
def test_same_second_superset_operation_leaves_other_pair_intact(
    client, clean_db, exercise_factory, workout_plan_factory, monkeypatch,
    legacy, operation, pair_index,
):
    ids, first_group, second_group = _same_second_pairs(
        client, clean_db, exercise_factory, workout_plan_factory, monkeypatch,
        legacy=legacy,
    )
    target = ids[pair_index * 2]
    untouched_ids = ids[2:] if pair_index == 0 else ids[:2]
    untouched_group = second_group if pair_index == 0 else first_group
    if operation == "unlink":
        response = client.post("/api/superset/unlink", json={"exercise_id": target})
        assert response.status_code == 200
        assert set(response.get_json()["data"]["unlinked_ids"]) == set(
            ids[pair_index * 2:pair_index * 2 + 2]
        )
    else:
        response = client.post("/remove_exercise", json={"id": target})
        assert response.status_code == 200
        assert clean_db.fetch_one(
            "SELECT id FROM user_selection WHERE id = ?", (target,),
        ) is None
    partner = ids[pair_index * 2 + 1]
    assert clean_db.fetch_one(
        "SELECT superset_group FROM user_selection WHERE id = ?", (partner,),
    )["superset_group"] is None
    for untouched_id in untouched_ids:
        assert clean_db.fetch_one(
            "SELECT superset_group FROM user_selection WHERE id = ?", (untouched_id,),
        )["superset_group"] == untouched_group


def test_antagonist_pairing_preserves_first_match_and_pair_order():
    from utils.supersets import _find_antagonist_pairings

    exercises = [
        {
            "id": 1,
            "exercise": "Chest One",
            "primary_muscle_group": "Chest",
            "superset_group": None,
        },
        {
            "id": 2,
            "exercise": "Back One",
            "primary_muscle_group": "Upper Back",
            "superset_group": None,
        },
        {
            "id": 3,
            "exercise": "Back Two",
            "primary_muscle_group": "Latissimus Dorsi",
            "superset_group": None,
        },
        {
            "id": 4,
            "exercise": "Chest Two",
            "primary_muscle_group": "Chest",
            "superset_group": None,
        },
        {
            "id": 5,
            "exercise": "Excluded Chest",
            "primary_muscle_group": "Chest",
            "superset_group": "SS-existing",
        },
    ]

    suggestions = _find_antagonist_pairings("A", exercises)

    assert [
        (item['exercise_1']['id'], item['exercise_2']['id'])
        for item in suggestions
    ] == [(1, 2), (3, 4)]
    assert suggestions[0] == {
        "routine": "A",
        "exercise_1": {"id": 1, "name": "Chest One", "muscle": "Chest"},
        "exercise_2": {
            "id": 2,
            "name": "Back One",
            "muscle": "Upper Back",
        },
        "reason": (
            "Antagonist pair: Chest / Upper Back - allows one muscle to rest "
            "while the other works"
        ),
        "benefit": "Saves time without compromising performance",
    }
