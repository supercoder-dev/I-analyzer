from operator import itemgetter


def test_rechtspraak_sources(test_corpus):
    s = test_corpus.sources()
    assert next(s)


def test_rechtspraak_documents(test_corpus, corpus_test_data):
    docs = sorted(list(test_corpus.documents()), key=itemgetter('date'))
    assert len(docs) == 2
    assert docs[0] == corpus_test_data['docs'][0]
    assert docs[1] == corpus_test_data['docs'][1]


def test_rechtspraak_required_fields(test_corpus):
    docs = test_corpus.documents()
    assert len(list(docs)) == 1
