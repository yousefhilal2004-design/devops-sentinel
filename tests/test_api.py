def test_root(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["application"] == "DevOps Sentinel"


def test_health(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_create_service(client):
    response = client.post(
        "/services",
        json={
            "name": "Example Website",
            "url": "https://example.com",
        },
    )

    assert response.status_code == 201
    assert response.json()["id"] == 1
    assert response.json()["enabled"] is True


def test_list_services(client):
    client.post(
        "/services",
        json={
            "name": "Example Website",
            "url": "https://example.com",
        },
    )

    response = client.get("/services")

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_missing_service(client):
    response = client.get("/services/999")

    assert response.status_code == 404


def test_duplicate_service(client):
    payload = {
        "name": "Example Website",
        "url": "https://example.com",
    }

    first = client.post(
        "/services",
        json=payload,
    )

    second = client.post(
        "/services",
        json=payload,
    )

    assert first.status_code == 201
    assert second.status_code == 409


def test_reject_unapproved_host(client):
    response = client.post(
        "/services",
        json={
            "name": "Unapproved",
            "url": "https://unapproved.invalid",
        },
    )

    assert response.status_code == 422


def test_disable_service(client):
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
    assert response.json()["enabled"] is False


def test_checks_initially_empty(client):
    response = client.get("/checks")

    assert response.status_code == 200
    assert response.json() == []


def test_delete_service(client):
    created = client.post(
        "/services",
        json={
            "name": "Example Website",
            "url": "https://example.com",
        },
    ).json()

    response = client.delete(f"/services/{created['id']}")

    assert response.status_code == 204

    response = client.get(f"/services/{created['id']}")

    assert response.status_code == 404
