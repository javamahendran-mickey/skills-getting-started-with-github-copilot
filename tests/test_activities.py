import pytest


class TestGetActivities:
    """Tests for GET /activities endpoint."""

    def test_get_activities_returns_200(self, client):
        """Test that GET /activities returns status 200."""
        # Arrange
        
        # Act
        response = client.get("/activities")
        
        # Assert
        assert response.status_code == 200

    def test_get_activities_returns_dict(self, client):
        """Test that GET /activities returns a dictionary."""
        # Arrange
        
        # Act
        response = client.get("/activities")
        
        # Assert
        assert isinstance(response.json(), dict)

    def test_get_activities_contains_expected_fields(self, client):
        """Test that activities have required fields."""
        # Arrange
        required_fields = {"description", "schedule", "max_participants", "participants"}
        
        # Act
        response = client.get("/activities")
        activities = response.json()
        
        # Assert
        assert len(activities) > 0
        for activity_name, activity_data in activities.items():
            assert isinstance(activity_name, str)
            assert required_fields.issubset(activity_data.keys())
            assert isinstance(activity_data["participants"], list)

    def test_get_activities_has_known_activities(self, client):
        """Test that expected activities exist."""
        # Arrange
        expected_activities = {
            "Chess Club",
            "Programming Class",
            "Gym Class",
            "Volleyball",
            "Track and Field"
        }
        
        # Act
        response = client.get("/activities")
        activities = response.json()
        
        # Assert
        for activity in expected_activities:
            assert activity in activities

    def test_activity_description_is_string(self, client):
        """Test that activity descriptions are non-empty strings."""
        # Arrange
        
        # Act
        response = client.get("/activities")
        activities = response.json()
        
        # Assert
        for activity_data in activities.values():
            assert isinstance(activity_data["description"], str)
            assert len(activity_data["description"]) > 0

    def test_activity_max_participants_is_positive_integer(self, client):
        """Test that max_participants is a positive integer."""
        # Arrange
        
        # Act
        response = client.get("/activities")
        activities = response.json()
        
        # Assert
        for activity_data in activities.values():
            assert isinstance(activity_data["max_participants"], int)
            assert activity_data["max_participants"] > 0

    def test_participants_are_valid_emails(self, client):
        """Test that participants are valid email addresses."""
        # Arrange
        
        # Act
        response = client.get("/activities")
        activities = response.json()
        
        # Assert
        for activity_data in activities.values():
            for participant in activity_data["participants"]:
                assert isinstance(participant, str)
                assert "@" in participant
