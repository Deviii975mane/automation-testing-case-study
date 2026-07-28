"""Loads environment and browser configuration from YAML files."""
import os
import yaml

CONFIG_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "config")


def _load_yaml(filename: str) -> dict:
    path = os.path.join(CONFIG_DIR, filename)
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_environment(name: str = "company1") -> dict:
    """Return config for a tenant environment."""
    data = _load_yaml("environments.yaml")
    if name not in data:
        raise ValueError(f"Unknown environment: {name}")
    return data[name]


def load_browsers() -> dict:
    return _load_yaml("browsers.yaml")