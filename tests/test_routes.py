from app.models import User, Folder, Bookmark, db

def login(client, username):
    return client.post(
        "/auth/login",
        data={"username": username},
        follow_redirects=True
    )

def login(client, username="testuser"):
    return client.post("/auth/login", data={"username": username}, follow_redirects=True)


def test_login_route(client):
    response = login(client)
    assert b"Welcome" in response.data or b"Bookmarks" in response.data


def test_protected_bookmarks_requires_login(client):
    response = client.get("/bookmarks", follow_redirects=True)
    # Should redirect to login page
    assert b"Login" in response.data


def test_create_folder_route(client):
    login(client)
    response = client.post("/folders/add", data={"name": "New Folder"}, follow_redirects=True)

    assert b"Folder" in response.data
    assert Folder.query.filter_by(name="New Folder").first() is not None


def test_add_bookmark_with_folder(client):
    login(client)

    folder = Folder(name="My Folder", user_id=1)
    db.session.add(folder)
    db.session.commit()

    response = client.post(
        "/bookmarks/add",
        data={
            "title": "Google",
            "url": "https://google.com",
            "folder_id": folder.id
        },
        follow_redirects=True
    )

    assert b"Google" in response.data
    assert Bookmark.query.filter_by(title="Google").first().folder_id == folder.id

from app.models import Course, Assignment, db

def test_instructor_can_create_assignment(client):
    login(client, "instructor")

    # Create course directly in DB
    course = Course(
        title="Math",
        description="Calculus",
        instructor_id=User.query.filter_by(username="instructor").first().id
    )
    db.session.add(course)
    db.session.commit()

    response = client.post(
        f"/courses/{course.id}/assignments/new",
        data={
            "title": "Homework 1",
            "description": "Limits"
        },
        follow_redirects=True
    )

    assert b"Homework 1" in response.data


def test_student_cannot_create_assignment(client):
    login(client, "testuser")

    # Create a course owned by instructor
    instructor = User.query.filter_by(username="instructor").first()

    course = Course(
        title="Test Course",
        description="Test Description",
        instructor_id=instructor.id
    )
    db.session.add(course)
    db.session.commit()

    response = client.post(
        f"/courses/{course.id}/assignments/new",
        data={
            "title": "Illegal HW",
            "description": "Should fail"
        },
        follow_redirects=True
    )

    assert b"Only the course instructor" in response.data


def test_instructor_can_create_course(client):
    login(client, "instructor")

    response = client.post(
        "/courses/new",
        data={
            "title": "Physics",
            "description": "Mechanics"
        },
        follow_redirects=True
    )

    assert b"Physics" in response.data


def test_student_cannot_create_course(client):
    login(client, "testuser")

    response = client.post(
        "/courses/new",
        data={
            "title": "Chemistry",
            "description": "Organic"
        },
        follow_redirects=True
    )

    # Should be blocked and redirected
    assert b"Only instructors can create courses" in response.data


def test_edit_bookmark(client):
    login(client, "testuser")

    bm = Bookmark(
        title="Old",
        url="https://old.com",
        user_id=1
    )
    db.session.add(bm)
    db.session.commit()

    response = client.post(
        f"/bookmarks/edit/{bm.id}",
        data={
            "title": "New",
            "url": "https://new.com"
        },
        follow_redirects=True
    )

    updated = Bookmark.query.get(bm.id)
    assert updated.title == "New"

def test_delete_bookmark(client):
    login(client, "testuser")

    bm = Bookmark(
        title="Delete Me",
        url="https://delete.com",
        user_id=1
    )
    db.session.add(bm)
    db.session.commit()

    response = client.post(
        f"/bookmarks/delete/{bm.id}",
        follow_redirects=True
    )

    assert Bookmark.query.get(bm.id) is None

def test_delete_folder(client):
    login(client, "testuser")

    folder = Folder(name="Temp", user_id=1)
    db.session.add(folder)
    db.session.commit()

    response = client.post(
        f"/folders/delete/{folder.id}",
        follow_redirects=True
    )

    assert Folder.query.get(folder.id) is None

def test_course_detail_page(client):
    login(client, "instructor")

    course = Course(
        title="Test Course",
        description="Test",
        instructor_id=2
    )
    db.session.add(course)
    db.session.commit()

    response = client.get(f"/courses/{course.id}")
    assert response.status_code == 200

def test_delete_course(client):
    login(client, "instructor")

    course = Course(
        title="Delete Course",
        description="Test",
        instructor_id=2
    )
    db.session.add(course)
    db.session.commit()

    response = client.post(
        f"/courses/{course.id}/delete",
        follow_redirects=True
    )

    assert Course.query.get(course.id) is None

def test_delete_assignment(client):
    login(client, "instructor")

    course = Course(
        title="Course",
        description="Desc",
        instructor_id=2
    )
    db.session.add(course)
    db.session.commit()

    assignment = Assignment(
        title="HW",
        description="Desc",
        course_id=course.id
    )
    db.session.add(assignment)
    db.session.commit()

    response = client.post(
        f"/assignments/{assignment.id}/delete",
        follow_redirects=True
    )

    assert Assignment.query.get(assignment.id) is None

def test_index_page(client):
    response = client.get("/")
    assert response.status_code == 200


def test_feature_page(client):
    response = client.get("/feature")
    assert response.status_code == 200

def test_bookmarks_page(client):
    login(client, "testuser")
    response = client.get("/bookmarks")
    assert response.status_code == 200





