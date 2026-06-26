import pytest


class TestDeleteParticipant:
    """Tests for DELETE /activities/{activity_name}/participants/{email} endpoint."""

    def test_delete_valid_participant_returns_200(self, client):
        """Test deleting valid participant returns 200."""
        # Arrange
        email = "toremove@mergington.edu"
        activity = "Programming Class"
        # Setup: Add participant first
        client.post(
            f"/activities/{activity.replace(' ', '%20')}/signup?email={email}",
            json={}
        )
        
        # Act
        response = client.delete(
            f"/activities/{activity.replace(' ', '%20')}/participants/{email}"
        )
        
        # Assert
        assert response.status_code == 200

    def test_delete_returns_success_message(self, client):
        """Test delete returns success message."""
        # Arrange
        email = "removetest@mergington.edu"
        activity = "Art Club"
        client.post(
            f"/activities/{activity.replace(' ', '%20')}/signup?email={email}",
            json={}
        )
        
        # Act
        response = client.delete(
            f"/activities/{activity.replace(' ', '%20')}/participants/{email}"
        )
        
        # Assert
        data = response.json()
        assert "message" in data
        assert "Removed" in data["message"]
        assert email in data["message"]

    def test_delete_invalid_activity_returns_404(self, client):
        """Test deleting from non-existent activity returns 404."""
        # Arrange
        invalid_activity = "NonExistent"
        email = "student@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{invalid_activity}/participants/{email}"
        )
        
        # Assert
        assert response.status_code == 404

    def test_delete_non_existent_participant_returns_400(self, client):
        """Test deleting non-existent participant returns 400."""
        # Arrange
        email = "notreal@mergington.edu"
        activity = "Chess Club"
        
        # Act
        response = client.delete(
            f"/activities/{activity.replace(' ', '%20')}/participants/{email}"
        )
        
        # Assert
        assert response.status_code == 400
        assert "not found" in response.json()["detail"].lower()

    def test_delete_removes_from_participant_list(self, client):
        """Test that delete actually removes participant."""
        # Arrange
        email = "deletecheck@mergington.edu"
        activity = "Volleyball"
        client.post(
            f"/activities/{activity.replace(' ', '%20')}/signup?email={email}",
            json={}
        )
        
        # Verify setup
        before = client.get("/activities").json()
        assert email in before[activity]["participants"]
        
        # Act
        client.delete(
            f"/activities/{activity.replace(' ', '%20')}/participants/{email}"
        )
        
        # Assert
        after = client.get("/activities").json()
        assert email not in after[activity]["participants"]

    def test_delete_same_participant_twice_returns_400(self, client):
        """Test deleting same participant twice returns 400 on second attempt."""
        # Arrange
        email = "doubledelete@mergington.edu"
        activity = "Drama Workshop"
        client.post(
            f"/activities/{activity.replace(' ', '%20')}/signup?email={email}",
            json={}
        )
        
        # Act - First delete
        response1 = client.delete(
            f"/activities/{activity.replace(' ', '%20')}/participants/{email}"
        )
        
        # Act - Second delete
        response2 = client.delete(
            f"/activities/{activity.replace(' ', '%20')}/participants/{email}"
        )
        
        # Assert
        assert response1.status_code == 200
        assert response2.status_code == 400

    def test_delete_with_url_encoded_email(self, client):
        """Test delete with special characters in email."""
        # Arrange
        email = "special+chars@mergington.edu"
        activity = "Track and Field"
        client.post(
            f"/activities/{activity.replace(' ', '%20')}/signup?email={email}",
            json={}
        )
        
        # Act
        encoded_email = "special%2Bchars@mergington.edu"
        response = client.delete(
            f"/activities/{activity.replace(' ', '%20')}/participants/{encoded_email}"
        )
        
        # Assert
        assert response.status_code == 200

    def test_delete_does_not_affect_other_activities(self, client):
        """Test that deleting from one activity doesn't affect others."""
        # Arrange
        email = "isolateddelete@mergington.edu"
        activity1 = "Science Olympiad"
        activity2 = "Debate Team"
        client.post(
            f"/activities/{activity1.replace(' ', '%20')}/signup?email={email}",
            json={}
        )
        client.post(
            f"/activities/{activity2.replace(' ', '%20')}/signup?email={email}",
            json={}
        )
        
        # Act - Delete from first activity
        client.delete(
            f"/activities/{activity1.replace(' ', '%20')}/participants/{email}"
        )
        
        # Assert
        activities = client.get("/activities").json()
        assert email not in activities[activity1]["participants"]
        assert email in activities[activity2]["participants"]
