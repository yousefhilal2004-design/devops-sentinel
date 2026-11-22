import httpx

from worker import main as worker

TEST_SERVICE = {
    "id": 1,
    "name": "Example Website",
    "url": "https://example.com",
}


def make_client(status_code):
    def handler(request):
        return httpx.Response(
            status_code=status_code,
            request=request,
        )

    return httpx.Client(
        transport=httpx.MockTransport(handler),
        follow_redirects=False,
        trust_env=False,
    )


def test_successful_http_check(monkeypatch):
    monkeypatch.setattr(
        worker,
        "validate_target",
        lambda url: url,
    )

    with make_client(200) as client:
        result = worker.check_service(
            TEST_SERVICE,
            client,
        )

    assert result["status"] == "up"
    assert result["status_code"] == 200
    assert result["response_time_ms"] >= 0
    assert result["error_message"] is None


def test_http_500_is_down(monkeypatch):
    monkeypatch.setattr(
        worker,
        "validate_target",
        lambda url: url,
    )

    with make_client(500) as client:
        result = worker.check_service(
            TEST_SERVICE,
            client,
        )

    assert result["status"] == "down"
    assert result["status_code"] == 500


def test_http_404_is_down(monkeypatch):
    monkeypatch.setattr(
        worker,
        "validate_target",
        lambda url: url,
    )

    with make_client(404) as client:
        result = worker.check_service(
            TEST_SERVICE,
            client,
        )

    assert result["status"] == "down"
    assert result["status_code"] == 404


def test_redirect_is_down(monkeypatch):
    monkeypatch.setattr(
        worker,
        "validate_target",
        lambda url: url,
    )

    with make_client(301) as client:
        result = worker.check_service(
            TEST_SERVICE,
            client,
        )

    assert result["status"] == "down"
    assert result["status_code"] == 301


def test_unapproved_target_is_rejected(monkeypatch):
    def reject_target(url):
        raise ValueError("Hostname is not approved")

    monkeypatch.setattr(
        worker,
        "validate_target",
        reject_target,
    )

    with make_client(200) as client:
        result = worker.check_service(
            TEST_SERVICE,
            client,
        )

    assert result["status"] == "down"
    assert result["status_code"] is None
    assert "not approved" in result["error_message"]


def test_timeout_is_down(monkeypatch):
    monkeypatch.setattr(
        worker,
        "validate_target",
        lambda url: url,
    )

    def timeout_handler(request):
        raise httpx.ReadTimeout(
            "Request timed out",
            request=request,
        )

    with httpx.Client(
        transport=httpx.MockTransport(timeout_handler),
        trust_env=False,
    ) as client:
        result = worker.check_service(
            TEST_SERVICE,
            client,
        )

    assert result["status"] == "down"
    assert result["status_code"] is None
    assert "ReadTimeout" in result["error_message"]


def test_disabled_services_are_excluded(client):
    created = client.post(
        "/services",
        json={
            "name": "Example Website",
            "url": "https://example.com",
        },
    ).json()

    response = client.patch(
        f"/services/{created['id']}",
        json={"enabled": False},
    )

    assert response.status_code == 200

    services = worker.get_enabled_services()

    assert services == []


def test_worker_saves_monitoring_result(
    client,
    monkeypatch,
):
    created = client.post(
        "/services",
        json={
            "name": "Example Website",
            "url": "https://example.com",
        },
    ).json()

    def fake_check(service, http_client):
        return {
            "service_id": service["id"],
            "status": "up",
            "status_code": 200,
            "response_time_ms": 42.5,
            "error_message": None,
        }

    monkeypatch.setattr(
        worker,
        "check_service",
        fake_check,
    )

    worker.run_cycle()

    response = client.get(f"/services/{created['id']}/checks")

    assert response.status_code == 200

    checks = response.json()

    assert len(checks) == 1
    assert checks[0]["status"] == "up"
    assert checks[0]["status_code"] == 200
    assert checks[0]["response_time_ms"] == 42.5
