import pytest


class TestSignup:
    """Tests for POST /activities/{activity_name}/signup endpoint."""

    def test_signup_valid_activity_returns_200(self, client):
        """Test successful signup returns 200."""
        # Arrange
        email = "newstudent@mergington.edu"
        activity = "Chess Club"
        
        # Act
        response = client.post(
            f"/activities/{activity.replace(' ', '%20')}/signup?email={email}",
            json={}
        )
        
        # Assert
        assert response.status_code == 200

    def test_signup_valid_activity_returns_success_message(self, client):
        """Test signup returns success message."""
        # Arrange
        email = "student123@mergington.edu"
        activity = "Art Club"
        expected_keywords = {"Signed up", email, activity}
        
        # Act
        response = client.post(
            f"/activities/{activity.replace(' ', '%20')}/signup?email={email}",
            json={}
        )
        data = response.json()
        
        # Assert
        assert "message" in data
        assert any(keyword in data["message"] for keyword in expected_keywords)

    def test_signup_invalid_activity_returns_404(self, client):
        """Test signup for non-existent activity returns 404."""
        # Arrange
        invalid_activity = "NonExistent Activity"
        email = "student@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{invalid_activity.replace(' ', '%20')}/signup?email={email}",
            json={}
        )
        
        # Assert
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    def test_signup_duplicate_student_returns_400(self, client):
        """Test signing up same student twice returns 400."""
        # Arrange
        email = "duplicate@mergington.edu"
        activity = "Drama Workshop"
        
        # Act - First signup
        response1 = client.post(
            f"/activities/{activity.replace(' ', '%20')}/signup?email={email}",
            json={}
        )
        
        # Act - Second signup with same email
        response2 = client.post(
            f"/activities/{activity.replace(' ', '%20')}/signup?email={email}",
            json={}
        )
        
        # Assert
        assert response1.status_code == 200
        assert response2.status_code == 400
        assert "already signed up" in response2.json()["detail"].lower()

    def test_signup_updates_participant_list(self, client):
        """Test that signup adds participant to activity."""
        # Arrange
        email = "newparticipant@mergington.edu"
        activity = "Science Olympiad"
        before = client.get("/activities").json()
        participants_before = len(before[activity]["participants"])
        
        # Act
        client.post(
            f"/activities/{activity.replace(' ', '%20')}/signup?email={email}",
            json={}
        )
        
        # Assert
        after = client.get("/activities").json()
        participants_after = len(after[activity]["participants"])
        assert participants_after == participants_before + 1
        assert email in after[activity]["participants"]

    def test_signup_same_student_different_activities(self, client):
        """Test that same student can signup for different activities."""
        # Arrange
        email = "multiactivity@mergington.edu"
        activity1 = "Debate Team"
        activity2 = "Volleyball"
        
        # Act - Signup for first activity
        response1 = client.post(
            f"/activities/{activity1.replace(' ', '%20')}/signup?email={email}",
            json={}
        )
        
        # Act - Signup for second activity
        response2 = client.post(
            f"/activities/{activity2.replace(' ', '%20')}/signup?email={email}",
            json={}
        )
        
        # Assert
        assert response1.status_code == 200
        assert response2.status_code == 200
        activities = client.get("/activities").json()
        assert email in activities[activity1]["participants"]
        assert email in activities[activity2]["participants"]

    def test_signup_case_sensitive_activity_names(self, client):
        """Test that activity names are case-sensitive."""
        # Arrange
        invalid_activity = "chess club"
        email = "student@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{invalid_activity.replace(' ', '%20')}/signup?email={email}",
            json={}
        )
        
        # Assert
        assert response.status_code == 404

    def test_signup_with_special_characters_in_email(self, client):
        """Test signup with special characters in email."""
        # Arrange
        email = "student+test@mergington.edu"
        activity = "Track and Field"
        
        # Act
        response = client.post(
            f"/activities/{activity.replace(' ', '%20')}/signup?email={email}",
            json={}
        )
        
        # Assert
        assert response.status_code == 200
        activities = client.get("/activities").json()
        assert email in activities[activity]["participants"]
