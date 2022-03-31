
from ianalyzer.conftest import client, db, times_user, session
import pytest

@pytest.fixture
def date_term_frequency_body(basic_query):
    return {
        'es_query': basic_query,
        'corpus_name': 'mock-corpus',
        'field_name': 'date',
        'start_date': '1850-01-01',
        'end_date': '1859-12-31',
        'size': 10,
    }

@pytest.fixture
def aggregate_term_frequency_body(basic_query):
    return {
        'es_query': basic_query,
        'corpus_name': 'mock-corpus',
        'field_name': 'genre',
        'field_value': 'Romance',
        'size': 10,
    }

@pytest.fixture
def ngram_body(basic_query):
    return {
        'es_query': basic_query,
        'corpus_name': 'mock-corpus',
        'field_name': 'content',
        'ngram_size': 2,
        'term_position': [0, 1],
        'freq_compensation': True,
        'subfield': 'clean',
        'max_size_per_interval': 2
    }

@pytest.mark.usefixtures("client", "times_user", "session")
def test_ngrams(client, test_app, ngram_body):
    client.times_login()
    post_response = client.post('/api/ngrams', json=ngram_body)
    assert post_response.status_code == 200

@pytest.mark.usefixtures("client", "times_user", "session")
def test_aggregate_term_frequency(client, test_app, aggregate_term_frequency_body):
    client.times_login()
    post_response = client.post('/api/aggregate_term_frequency', json=aggregate_term_frequency_body)
    assert post_response.status_code == 200

@pytest.mark.usefixtures("client", "times_user", "session")
def test_date_term_frequency(client, test_app, date_term_frequency_body):
    client.times_login()
    post_response = client.post('/api/date_term_frequency', json=date_term_frequency_body)
    assert post_response.status_code == 200
