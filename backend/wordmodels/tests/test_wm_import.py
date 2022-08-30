from wordmodels.utils import load_word_models, word_in_model
from wordmodels.conftest import TEST_VOCAB_SIZE, TEST_DIMENSIONS, TEST_BINS

def test_complete_import(test_app):
    model = load_word_models('mock-corpus')
    assert model

    weights = model['svd_ppmi']
    assert weights.shape == (TEST_DIMENSIONS, TEST_VOCAB_SIZE)

    transformer = model['transformer']
    assert transformer.max_features == TEST_VOCAB_SIZE

def test_binned_import(test_app):
    models = load_word_models('mock-corpus', binned = True)
    assert len(models) == len(TEST_BINS)

    for model, bin in zip(models, TEST_BINS):
        start_year, end_year = bin

        assert model['start_year'] == start_year
        assert model['end_year'] == end_year

        weights = model['svd_ppmi']
        assert weights.shape == (TEST_DIMENSIONS, TEST_VOCAB_SIZE)

        transformer = model['transformer']
        assert transformer.max_features == TEST_VOCAB_SIZE

def test_word_in_model(test_app):
    cases = [
        {
            'term': 'she',
            'expected': {'exists': True}
        },
        {
            'term':  'whale',
            'expected': {'exists': True}
        },
                {
            'term':  'hwale',
            'expected': {'exists': False, 'similar_keys': ['whale']}
        }
    ]

    for case in cases:
        result = word_in_model(case['term'], 'mock-corpus', 1)
        assert result == case['expected']
