from fastapi.testclient import TestClient

from src.app import activities, app


client = TestClient(app)
activity_name = "Chess Club"
student_email = "new-student@mergington.edu"


def setup_function():
    client.cookies.clear()
    participants = activities[activity_name]["participants"]
    if student_email in participants:
        participants.remove(student_email)


def login(username="teacher", password="mergington2026"):
    return client.post(
        "/auth/login", json={"username": username, "password": password}
    )


def test_students_can_view_activities_without_login():
    response = client.get("/activities")

    assert response.status_code == 200
    assert activity_name in response.json()


def test_anonymous_user_cannot_change_registrations():
    signup_response = client.post(
        f"/activities/{activity_name}/signup", params={"email": student_email}
    )
    unregister_response = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": "michael@mergington.edu"},
    )

    assert signup_response.status_code == 401
    assert unregister_response.status_code == 401
    assert student_email not in activities[activity_name]["participants"]
    assert "michael@mergington.edu" in activities[activity_name]["participants"]


def test_invalid_login_is_rejected():
    response = login(password="incorrect")

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid username or password"


def test_teacher_can_signup_and_unregister_student():
    login_response = login()
    signup_response = client.post(
        f"/activities/{activity_name}/signup", params={"email": student_email}
    )
    unregister_response = client.delete(
        f"/activities/{activity_name}/unregister", params={"email": student_email}
    )

    assert login_response.status_code == 200
    assert signup_response.status_code == 200
    assert unregister_response.status_code == 200
    assert student_email not in activities[activity_name]["participants"]


def test_logout_revokes_access():
    login()

    logout_response = client.post("/auth/logout")
    signup_response = client.post(
        f"/activities/{activity_name}/signup", params={"email": student_email}
    )

    assert logout_response.status_code == 200
    assert signup_response.status_code == 401