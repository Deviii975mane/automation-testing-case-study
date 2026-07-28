"""API tests for the Projects service, including tenant isolation."""
import uuid
import pytest

from src.api.projects_client import ProjectsClient
from src.utils.config_loader import load_environment


@pytest.fixture
def projects_client():
    return ProjectsClient()


@pytest.fixture
def created_project(projects_client):
    """Create a project via API and clean it up afterwards."""
    env = load_environment("company1")
    tenant_id = env["tenant_id"]
    name = f"API Project {uuid.uuid4().hex[:8]}"

    resp = projects_client.create_project(tenant_id, name, "api test")
    assert resp.status_code in (200, 201), f"Create failed: {resp.text}"
    project = resp.json()
    project["tenant_id"] = tenant_id

    yield project

    projects_client.delete_project(tenant_id, project["id"])


@pytest.mark.api
def test_create_project(created_project):
    assert created_project["id"] is not None
    assert created_project["status"] == "active"


@pytest.mark.api
def test_get_project(projects_client, created_project):
    resp = projects_client.get_project(
        created_project["tenant_id"], created_project["id"]
    )
    assert resp.status_code == 200
    assert resp.json()["name"] == created_project["name"]


@pytest.mark.api
@pytest.mark.security
def test_tenant_isolation_api(projects_client, created_project):
    """Company2 must NOT be able to read Company1's project."""
    other_tenant = load_environment("company2")["tenant_id"]
    resp = projects_client.get_project(other_tenant, created_project["id"])
    assert resp.status_code in (403, 404), (
        f"Tenant isolation breach! Got {resp.status_code}"
    )