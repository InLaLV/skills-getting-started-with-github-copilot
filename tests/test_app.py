import pytest
from src.app import activities

class TestActivitiesAPI:
    """Test suite for Activities API endpoints"""

    @pytest.mark.asyncio
    async def test_get_activities(self, client):
        """Test GET /activities returns all activities"""
        # Arrange
        # (client fixture provides TestClient)

        # Act
        response = await client.get("/activities")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert "Chess Club" in data
        assert "Programming Class" in data
        # Verify structure of one activity
        chess_club = data["Chess Club"]
        assert "description" in chess_club
        assert "schedule" in chess_club
        assert "max_participants" in chess_club
        assert "participants" in chess_club
        assert isinstance(chess_club["participants"], list)

    @pytest.mark.asyncio
    async def test_root_redirect(self, client):
        """Test GET / redirects to static index"""
        # Arrange
        # (client fixture provides TestClient)

        # Act
        response = await client.get("/")

        # Assert
        assert response.status_code == 307  # Temporary redirect
        assert response.headers["location"] == "/static/index.html"

    @pytest.mark.asyncio
    async def test_signup_success(self, client):
        """Test POST /activities/{activity_name}/signup successful signup"""
        # Arrange
        activity_name = "Chess Club"
        email = "test@mergington.edu"
        initial_count = len(activities[activity_name]["participants"])

        # Act
        response = await client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert f"Signed up {email} for {activity_name}" in data["message"]
        # Verify participant was added
        assert email in activities[activity_name]["participants"]
        assert len(activities[activity_name]["participants"]) == initial_count + 1

    @pytest.mark.asyncio
    async def test_signup_activity_not_found(self, client):
        """Test POST /activities/{activity_name}/signup with non-existent activity"""
        # Arrange
        activity_name = "NonExistent Activity"
        email = "test@mergington.edu"

        # Act
        response = await client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "Activity not found" in data["detail"]

    @pytest.mark.asyncio
    async def test_signup_duplicate(self, client):
        """Test POST /activities/{activity_name}/signup duplicate signup"""
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already signed up
        initial_count = len(activities[activity_name]["participants"])

        # Act
        response = await client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert "Student already signed up" in data["detail"]
        # Verify no duplicate added
        assert len(activities[activity_name]["participants"]) == initial_count

    @pytest.mark.asyncio
    async def test_unregister_success(self, client):
        """Test DELETE /activities/{activity_name}/unregister successful unregister"""
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already signed up
        initial_count = len(activities[activity_name]["participants"])

        # Act
        response = await client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert f"Unregistered {email} from {activity_name}" in data["message"]
        # Verify participant was removed
        assert email not in activities[activity_name]["participants"]
        assert len(activities[activity_name]["participants"]) == initial_count - 1

    @pytest.mark.asyncio
    async def test_unregister_activity_not_found(self, client):
        """Test DELETE /activities/{activity_name}/unregister with non-existent activity"""
        # Arrange
        activity_name = "NonExistent Activity"
        email = "test@mergington.edu"

        # Act
        response = await client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "Activity not found" in data["detail"]

    @pytest.mark.asyncio
    async def test_unregister_student_not_registered(self, client):
        """Test DELETE /activities/{activity_name}/unregister student not registered"""
        # Arrange
        activity_name = "Chess Club"
        email = "notregistered@mergington.edu"  # Not signed up
        initial_count = len(activities[activity_name]["participants"])

        # Act
        response = await client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert "Student is not registered for this activity" in data["detail"]
        # Verify no change
        assert len(activities[activity_name]["participants"]) == initial_count