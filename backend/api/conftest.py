from time import sleep
import pytest
import os
from ianalyzer.factories.elasticsearch import elasticsearch
import ianalyzer.config_fallback as config
from ianalyzer.factories.app import flask_app
import es.es_index as index
from es.search import get_index
from addcorpus.load_corpus import load_corpus

here = os.path.abspath(os.path.dirname(__file__))

class UnittestConfig:
    SECRET_KEY = b'dd5520c21ee49d64e7f78d3220b2be1dde4eb4a0933c8baf'
    SQLALCHEMY_DATABASE_URI = 'sqlite://'  # in-memory
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
    TESTING = True
    CORPORA = {
        'mock-corpus': os.path.join(here, 'tests', 'mock_corpus.py'),
    }
    SERVERS = {
        'default': config.SERVERS['default']
    }
    CORPUS_SERVER_NAMES = {
        'mock-corpus': 'default',
    }
    CORPUS_DEFINITIONS = {}

    SAML_FOLDER = "saml"
    SAML_SOLISID_KEY = "uuShortID"
    SAML_MAIL_KEY = "mail"

@pytest.fixture(scope='session')
def celery_config():
    return {
        'broker_url': 'amqp://',
        'result_backend': 'amqp'
    }

@pytest.fixture(scope='session')
def test_app(request, tmpdir_factory):
    """ Provide an instance of the application with Flask's test_client. """
    app = flask_app(UnittestConfig)
    app.testing = True
    app.config['CSV_FILES_PATH'] = str(tmpdir_factory.mktemp('test_files'))

    with app.app_context():
        yield app

@pytest.fixture(scope='session')
def test_es_client(test_app):
    """
    Create and populate an index for the mock corpus in elasticsearch.
    Returns an elastic search client for the mock corpus.
    """
    client = elasticsearch('mock-corpus')
    # check if client is available, else skip test
    try:
        client.info()
    except:
        pytest.skip('Cannot connect to elasticsearch server')

    # add data from mock corpus
    corpus = load_corpus('mock-corpus')
    index.create(client, corpus, False, True, False)
    index.populate(client, 'mock-corpus', corpus)

    # ES is "near real time", so give it a second before we start searching the index
    sleep(1)

    yield client

    # delete index when done
    mock_index = get_index('mock-corpus')
    client.indices.delete(index=mock_index)


@pytest.fixture
def basic_query():
    return {
        "query": {
            "bool": {
                "must": {
                    "simple_query_string": {
                        "query": "test",
                        "lenient": True,
                        "default_operator": "or"
                    }
                },
                "filter": []
            }
        }
    }
