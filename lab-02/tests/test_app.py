import pytest

import app as app_module


@pytest.fixture
def client(tmp_path, monkeypatch):
    """Create isolated test client with a temporary files"""
    counter_file = tmp_path / "visits.txt"

    monkeypatch.setattr(app_module, "DATABASE_URL", None)
    monkeypatch.setattr(app_module, "COUNTER_FILE", counter_file)

    app_module.app.config["TESTING"] = True

    with app_module.app.test_client() as test_client:
        yield test_client


def test_health_returns_ok(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.data == b"ok\n"


def test_ready_reports_file_store(client):
    response = client.get("/ready")

    assert response.status_code == 200
    assert response.json["ready"] is True
    assert response.json["store"].startswith("file:")


def test_visits_counter_increments(client):
    first_response = client.get("/visits")
    second_response = client.get("/visits")

    assert first_response.status_code == 200
    assert first_response.json["visits"] == 1

    assert second_response.status_code == 200
    assert second_response.json["visits"] == 2


def test_ready_returns_503_when_store_is_unavailable(tmp_path, monkeypatch):
    blocked_parent = tmp_path / "not-a-directory"
    blocked_parent.write_text("this is a file")

    monkeypatch.setattr(app_module, "DATABASE_URL", None)
    monkeypatch.setattr(
        app_module,
        "COUNTER_FILE",
        blocked_parent / "visits.txt",
    )

    app_module.app.config["TESTING"] = True

    with app_module.app.test_client() as test_client:
        response = test_client.get("/ready")

    assert response.status_code == 503
    assert response.json["ready"] is False
