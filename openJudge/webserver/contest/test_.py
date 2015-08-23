import pytest


@pytest.mark.django_db
def test_contest_home_page(client):
    page = client.get('/')
    assert page.status_code == 200
