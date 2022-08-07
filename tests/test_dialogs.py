import pytest
import json
from datetime import datetime


def test_get_dialog_data(client):
    response = client.get('data/')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 4


def test_get_dialog_data_order(client):
    response = client.get('data/')
    assert response.status_code == 200
    data = json.loads(response.data)
    format_string = '%a, %m %b %Y %H:%M:%S GMT'
    for i in range(len(data) - 1):
        timestamp_1 = datetime.strptime(data[i]['dialog_timestamp'], format_string)
        timestamp_2 = datetime.strptime(data[i + 1]['dialog_timestamp'], format_string)
        assert timestamp_1 > timestamp_2 


@pytest.mark.parametrize(('customer_id', 'num_elements'), (
    (1, 2),
    (2, 1),
    (3, 1),
    (4, 0),
))
def test_get_dialog_data_customer_id(client, customer_id, num_elements):
    response = client.get('data/', query_string={'customerId': customer_id})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == num_elements


def test_get_dialog_data_customer_id_wrong_value(client):
    response = client.get('data/', query_string={'customerId': -1})
    assert response.status_code == 400


@pytest.mark.parametrize(('language', 'num_elements'), (
    ('en', 3),
    ('de', 1),
    ('fr', 0),
))
def test_get_dialog_data_language(client, language, num_elements):
    response = client.get('data/', query_string={'language': language})
    assert response.status_code == 200
    values = json.loads(response.data)
    assert len(values) == num_elements


def test_get_dialog_data_language_wrong_value(client):
    response = client.get('data/', query_string={'language': 'ch'})
    assert response.status_code == 400


@pytest.mark.parametrize(('customer_id', 'language', 'num_elements'), (
    (1, 'en', 2),
    (2, 'en', 1),
    (3, 'de', 1),
))
def test_get_dialog_data_all_parameters(client, customer_id, language, num_elements):
    response = client.get('data/', query_string={'customerId': customer_id, 'language': language})
    assert response.status_code == 200
    values = json.loads(response.data)
    assert len(values) == num_elements


def test_post_dialog_data_no_consent(client):
    response = client.post('data/1/3', data=json.dumps({'text': 'Text 13', 'language': 'en'}), content_type='application/json')
    assert response.status_code == 200

    response = client.post('consents/3', data=json.dumps({'consent': False}), content_type='application/json')
    assert response.status_code == 200

    response = client.get('data/')
    assert response.status_code == 200
    values = json.loads(response.data)
    assert len(values) == 4


def test_post_dialog_data_consent(client):
    response = client.post('data/1/3', data=json.dumps({'text': 'Text 13', 'language': 'en'}), content_type='application/json')
    assert response.status_code == 200
    response = client.post('data/1/3', data=json.dumps({'text': 'Text 13', 'language': 'en'}), content_type='application/json')
    assert response.status_code == 200

    response = client.post('consents/3', data=json.dumps({'consent': True}), content_type='application/json')
    assert response.status_code == 200

    response = client.get('data/')
    assert response.status_code == 200
    values = json.loads(response.data)
    assert len(values) == 6


def test_post_dialog_data_missing_parameters(client):
    # No text and language
    response = client.post('data/1/3', data=json.dumps({}), content_type='application/json')
    assert response.status_code == 400


def test_post_dialog_data_wrong_parameters(client):
    # Wrong types
    response = client.post('data/1/3', data=json.dumps({'text': 1, 'language': 'en'}), content_type='application/json')
    assert response.status_code == 400

    response = client.post('data/1/3', data=json.dumps({'text': 'Text 13', 'language': 3}), content_type='application/json')
    assert response.status_code == 400

    # Unsupported locale
    response = client.post('data/1/3', data=json.dumps({'text': 'Text 13', 'language': 'ch'}), content_type='application/json')
    assert response.status_code == 400
