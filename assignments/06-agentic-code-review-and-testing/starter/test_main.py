from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_create_and_list_habit():
    r = client.post("/habits", json={"name": "Read 20 minutes"})
    assert r.status_code == 200
    hid = r.json()["id"]
    r2 = client.get("/habits")
    assert r2.status_code == 200
    assert any(h["id"] == hid for h in r2.json())


def test_checkin_flow():
    hid = client.post("/habits", json={"name": "Stretch"}).json()["id"]
    r = client.post(f"/habits/{hid}/checkin", json={"day": "2026-09-22"})
    assert r.status_code == 200
    r2 = client.get(f"/habits/{hid}/checkins")
    assert r2.json() == ["2026-09-22"]


def test_checkin_unknown_habit_404():
    r = client.post("/habits/99999/checkin", json={"day": "2026-09-22"})
    assert r.status_code == 404


# --- Validation tests ---


def test_create_habit_empty_name_rejected():
    """Empty habit name must return 422."""
    r = client.post("/habits", json={"name": ""})
    assert r.status_code == 422


def test_create_habit_whitespace_only_rejected():
    """Whitespace-only habit name must return 422."""
    r = client.post("/habits", json={"name": "   "})
    assert r.status_code == 422


def test_checkin_invalid_date_rejected():
    """Malformed day value must return 422."""
    hid = client.post("/habits", json={"name": "Date test"}).json()["id"]
    r = client.post(f"/habits/{hid}/checkin", json={"day": "not-a-date"})
    assert r.status_code == 422


def test_checkin_wrong_date_format_rejected():
    """Date in wrong format (DD/MM/YYYY) must return 422."""
    hid = client.post("/habits", json={"name": "Format test"}).json()["id"]
    r = client.post(f"/habits/{hid}/checkin", json={"day": "22/09/2026"})
    assert r.status_code == 422


def test_valid_habit_and_checkin_still_work():
    """Sanity check: valid inputs still pass through."""
    hid = client.post("/habits", json={"name": "Valid habit"}).json()["id"]
    r = client.post(f"/habits/{hid}/checkin", json={"day": "2026-09-22"})
    assert r.status_code == 200


def test_checkin_requires_exact_date_format():
    habit = client.post("/habits", json={"name": "Date format review"})
    assert habit.status_code == 200
    hid = habit.json()["id"]

    for day in ("20260922", "2026-W39-2"):
        response = client.post(f"/habits/{hid}/checkin", json={"day": day})
        assert response.status_code == 422, f"{day} returned {response.status_code}"
        assert "YYYY-MM-DD" in response.text
