import factory
from django.contrib.auth.models import User
from django.test import Client
from pytest import fixture, mark


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = "admin"
    email = "admin@example.com"
    is_staff = True
    is_superuser = True

    @factory.post_generation
    def password(obj, create, extracted, **kwargs):
        if create:
            obj.set_password("password123")
            obj.save()


@fixture
def admin_user():
    return UserFactory()


@fixture
def client():
    return Client()


@mark.django_db
def test_admin_login(client, admin_user):
    response = client.post(
        "/admin/login/",
        {
            "username": "admin",
            "password": "password123",
        },
    )
    assert response.status_code == 302


@mark.django_db
def test_admin_list(client, admin_user):
    client.login(username="admin", password="password123")
    response = client.get("/admin/auth/user/")
    assert response.status_code == 200
    assert "admin" in response.content.decode()


@mark.django_db
def test_admin_change(client, admin_user):
    client.login(username="admin", password="password123")
    response = client.get(f"/admin/auth/user/{admin_user.id}/change/")
    assert response.status_code == 200
    assert "admin@example.com" in response.content.decode()
