"""Projects API client — create, get, delete projects per tenant."""
from src.api.base_client import BaseClient


class ProjectsClient(BaseClient):
    def create_project(self, tenant_id: str, name: str,
                       description: str = "", team_members=None):
        body = {
            "name": name,
            "description": description,
            "team_members": team_members or [],
        }
        return self._request("POST", "projects", tenant_id, json=body)

    def get_project(self, tenant_id: str, project_id: int):
        return self._request("GET", f"projects/{project_id}", tenant_id)

    def delete_project(self, tenant_id: str, project_id: int):
        return self._request("DELETE", f"projects/{project_id}", tenant_id)