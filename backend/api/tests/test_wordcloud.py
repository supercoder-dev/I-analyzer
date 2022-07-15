import api.analyze as analyze
from es import search
import pytest
import api.query as query
from datetime import datetime

def make_filtered_query():
        empty_query = {
            "query": {
                "bool": {
                    "filter": []
                }
            }
        }
        datefilter = query.make_date_filter(max_date = datetime(year = 1813, month=12, day=31))
        return query.add_filter(empty_query, datefilter)


def test_wordcloud(test_app, test_es_client):
    if not test_es_client:
            pytest.skip('No elastic search client')

    query = {
        "query": {
            "match_all": {}
        },
    }

    result = search.search(
        corpus = 'mock-corpus',
        query_model = query,
        size = 10
    )

    documents = search.hits(result)

    target_unfiltered = [
        { 'key': 'of', 'doc_count': 5 },
        { 'key': 'a', 'doc_count': 4 },
        { 'key': 'to', 'doc_count': 3 },
        { 'key': 'the', 'doc_count': 2 },
        { 'key': 'you', 'doc_count': 2 },
        { 'key': 'that', 'doc_count': 2 },
        { 'key': 'in', 'doc_count': 2 },
        { 'key': 'with', 'doc_count': 1 },
        { 'key': 'will', 'doc_count': 1 },
        { 'key': 'wife', 'doc_count': 1 },
        { 'key': 'which', 'doc_count': 1 },
        { 'key': 'was', 'doc_count': 1 },
        { 'key': 'want', 'doc_count': 1 },
        { 'key': 'very', 'doc_count': 1 },
        { 'key': 'universally', 'doc_count': 1 },
        { 'key': 'truth', 'doc_count': 1 },
        { 'key': 'tired', 'doc_count': 1 },
        { 'key': 'such', 'doc_count': 1 },
        { 'key': 'sitting', 'doc_count': 1 },
        { 'key': 'sister', 'doc_count': 1 },
        { 'key': 'single', 'doc_count': 1 },
        { 'key': 'rejoice', 'doc_count': 1 },
        { 'key': 'regarded', 'doc_count': 1 },
        { 'key': 'possession', 'doc_count': 1 },
        { 'key': 'on', 'doc_count': 1 },
        { 'key': 'nothing', 'doc_count': 1 },
        { 'key': 'no', 'doc_count': 1 },
        { 'key': 'must', 'doc_count': 1 },
        { 'key': 'man', 'doc_count': 1 },
        { 'key': 'it', 'doc_count': 1 },
        { 'key': 'is', 'doc_count': 1 },
        { 'key': 'her', 'doc_count': 1 },
        { 'key': 'hear', 'doc_count': 1 },
        { 'key': 'having', 'doc_count': 1 },
        { 'key': 'have', 'doc_count': 1 },
        { 'key': 'has', 'doc_count': 1 },
        { 'key': 'good', 'doc_count': 1 },
        { 'key': 'get', 'doc_count': 1 },
        { 'key': 'fortune', 'doc_count': 1 },
        { 'key': 'forebodings', 'doc_count': 1 },
        { 'key': 'evil', 'doc_count': 1 },
        { 'key': 'enterprise', 'doc_count': 1 },
        { 'key': 'do', 'doc_count': 1 },
        { 'key': 'disaster', 'doc_count': 1 },
        { 'key': 'commencement', 'doc_count': 1 },
        { 'key': 'by', 'doc_count': 1 },
        { 'key': 'beginning', 'doc_count': 1 },
        { 'key': 'be', 'doc_count': 1 },
        { 'key': 'bank', 'doc_count': 1 },
        { 'key': 'and', 'doc_count': 1 },
        { 'key': 'an', 'doc_count': 1 },
        { 'key': 'alice', 'doc_count': 1 },
        { 'key': 'acknowledge', 'doc_count': 1 },
        { 'key': 'accompanied', 'doc_count': 1 }
    ]

    output = analyze.make_wordcloud_data(documents, 'content')
    for item in target_unfiltered:
        term = item['key']
        doc_count = item['doc_count']
        for hit in output:
            if term == hit['key']:
                assert doc_count == hit['doc_count']

def test_wordcloud_filtered(test_app, test_es_client):
    """Test the word cloud on a query with date filter"""
    if not test_es_client:
        pytest.skip('No elastic search client')

    filtered_query = make_filtered_query()

    target_filtered = [
        { 'key': 'it', 'doc_count': 1 },
        { 'key': 'is', 'doc_count': 1 },
        { 'key': 'a', 'doc_count': 4 },
        { 'key': 'of', 'doc_count':  2 }
    ]

    result = search.search(
        corpus = 'mock-corpus',
        query_model = filtered_query,
        size = 10,
        client = test_es_client
    )

    documents = search.hits(result)
    output = analyze.make_wordcloud_data(documents, 'content')

    for item in target_filtered:
        term = item['key']
        doc_count = item['doc_count']
        print(term, doc_count)
        for hit in output:
            if term == hit['key']:
                assert doc_count == hit['doc_count']



