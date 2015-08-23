import pytest


@pytest.mark.django_db
def test_question_and_language_detail_url(client):
    response = client.get('/question/detail_list/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_question_home_page(client):
    response = client.get('/question/')
    assert response.status_code == 200
