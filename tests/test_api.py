def test_root_redirects_to_static_index(client):
    # Arrange
    path = "/"

    # Act
    response = client.get(path, follow_redirects=False)

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_returns_dictionary(client):
    # Arrange
    path = "/activities"

    # Act
    response = client.get(path)

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_adds_student_to_activity(client, activities_data):
    # Arrange
    activity_name = "Art Studio"
    email = "new.student@mergington.edu"
    path = f"/activities/{activity_name}/signup"
    initial_count = len(activities_data[activity_name]["participants"])

    # Act
    response = client.post(path, params={"email": email})

    # Assert
    assert response.status_code == 200
    assert activities_data[activity_name]["participants"][-1] == email
    assert len(activities_data[activity_name]["participants"]) == initial_count + 1


def test_signup_returns_404_for_unknown_activity(client):
    # Arrange
    path = "/activities/Unknown%20Club/signup"
    email = "student@mergington.edu"

    # Act
    response = client.post(path, params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_returns_400_for_duplicate_student(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    path = f"/activities/{activity_name}/signup"

    # Act
    response = client.post(path, params={"email": email})

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_signup_returns_400_when_activity_is_full(client, activities_data):
    # Arrange
    activity_name = "Debate Club"
    activities_data[activity_name]["max_participants"] = 1
    email = "late.student@mergington.edu"
    path = f"/activities/{activity_name}/signup"

    # Act
    response = client.post(path, params={"email": email})

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Activity is full"


def test_unregister_removes_student_from_activity(client, activities_data):
    # Arrange
    activity_name = "Music Band"
    email = "noah@mergington.edu"
    path = f"/activities/{activity_name}/participants"
    assert email in activities_data[activity_name]["participants"]

    # Act
    response = client.delete(path, params={"email": email})

    # Assert
    assert response.status_code == 200
    assert email not in activities_data[activity_name]["participants"]


def test_unregister_returns_404_for_unknown_activity(client):
    # Arrange
    path = "/activities/Unknown%20Club/participants"
    email = "student@mergington.edu"

    # Act
    response = client.delete(path, params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_returns_404_for_non_participant(client):
    # Arrange
    activity_name = "Tennis Club"
    email = "not.signed.up@mergington.edu"
    path = f"/activities/{activity_name}/participants"

    # Act
    response = client.delete(path, params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Student is not signed up for this activity"