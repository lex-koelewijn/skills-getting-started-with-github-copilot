import copy

import pytest
from fastapi.testclient import TestClient

import src.app as app_module


DEFAULT_ACTIVITIES = copy.deepcopy(app_module.activities)


@pytest.fixture(autouse=True)
def reset_activities_state():
    """Reset de globale activities-state voor elke test."""
    app_module.activities = copy.deepcopy(DEFAULT_ACTIVITIES)
    yield


@pytest.fixture
def client():
    return TestClient(app_module.app)


@pytest.fixture
def activities_data():
    return app_module.activities