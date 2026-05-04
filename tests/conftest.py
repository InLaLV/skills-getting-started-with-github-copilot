import pytest
from httpx import AsyncClient
from src.app import app, activities
import copy

# Original activities data for reset
ORIGINAL_ACTIVITIES = copy.deepcopy(activities)

@pytest.fixture
def client():
    """Test client fixture"""
    return AsyncClient(app=app, base_url="http://testserver")

@pytest.fixture(autouse=True)
def reset_activities():
    """Reset activities dict before each test"""
    global activities
    activities.clear()
    activities.update(copy.deepcopy(ORIGINAL_ACTIVITIES))