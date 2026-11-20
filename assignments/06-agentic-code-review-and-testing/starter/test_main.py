from datetime import date, timedelta

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


def test_streak_zero_no_checkins():
    """A new habit with no check-ins has streak 0."""
    hid = client.post("/habits", json={"name": "Streak zero"}).json()["id"]
    r = client.get(f"/habits/{hid}/streak")
    assert r.status_code == 200
    assert r.json()["streak"] == 0


def test_streak_zero_old_checkin():
    """A check-in from two days ago (with a gap today) gives streak 0."""
    hid = client.post("/habits", json={"name": "Old streak"}).json()["id"]
    two_days_ago = (date.today() - timedelta(days=2)).isoformat()
    client.post(f"/habits/{hid}/checkin", json={"day": two_days_ago})
    r = client.get(f"/habits/{hid}/streak")
    assert r.status_code == 200
    assert r.json()["streak"] == 0


def test_streak_today_only():
    """Check-in today → streak is 1."""
    hid = client.post("/habits", json={"name": "Today streak"}).json()["id"]
    today = date.today().isoformat()
    client.post(f"/habits/{hid}/checkin", json={"day": today})
    r = client.get(f"/habits/{hid}/streak")
    assert r.status_code == 200
    assert r.json()["streak"] == 1


def test_streak_consecutive_days():
    """Check-ins for today and the previous two days → streak is 3."""
    hid = client.post("/habits", json={"name": "Three day streak"}).json()["id"]
    for days_back in range(3):
        day = (date.today() - timedelta(days=days_back)).isoformat()
        client.post(f"/habits/{hid}/checkin", json={"day": day})
    r = client.get(f"/habits/{hid}/streak")
    assert r.status_code == 200
    assert r.json()["streak"] == 3


def test_streak_unknown_habit_404():
    r = client.get("/habits/99999/streak")
    assert r.status_code == 404


def test_streak_counts_duplicate_checkins_once():
    habit = client.post("/habits", json={"name": "Daily walk"})
    assert habit.status_code == 200
    hid = habit.json()["id"]

    today = date.today()
    yesterday = today - timedelta(days=1)
    for day in (today, today, yesterday):
        checkin = client.post(f"/habits/{hid}/checkin", json={"day": day.isoformat()})
        assert checkin.status_code == 200

    response = client.get(f"/habits/{hid}/streak")
    assert response.status_code == 200
    assert response.json()["streak"] == 2
