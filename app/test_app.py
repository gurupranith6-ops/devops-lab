import pytest
from unittest.mock import patch
import app as flask_app


@pytest.fixture
def client():
    flask_app.app.config["TESTING"] = True

    with patch("app.r", autospec=True) as mock_redis:
        mock_redis.incr.return_value = 42
        mock_redis.get.return_value = "42"

        with flask_app.app.test_client() as c:
            yield c


def test_health(client):
    res = client.get("/health")

    assert res.status_code == 200
    assert res.get_json()["status"] == "ok"


def test_index_increments_visits(client):
    res = client.get("/")

    assert res.status_code == 200

    data = res.get_json()

    assert "message" in data
    assert "visits" in data
    assert "hostname" in data
    assert data["visits"] == 42


def test_reset_zeros_counter(client):
    res = client.post("/reset")

    assert res.status_code == 200

    data = res.get_json()

    assert data["visits"] == 0


def test_reset_requires_post(client):
    res = client.get("/reset")

    assert res.status_code == 405


def test_stats_returns_full_info(client):
    res = client.get("/stats")

    assert res.status_code == 200

    data = res.get_json()

    assert "visits" in data
    assert "hostname" in data
    assert "redis_host" in data
