import numpy as np
import api.analyze as analyze

def test_cosine_similarity_vectors():
    cases = [
        {
            'v1': np.array([1.0, 1.0]),
            'v2': np.array([0.5, 0.5]),
            'similarity': 1.0
        },
        {
            'v1': np.array([1.0, 0.0]),
            'v2': np.array([0.0, 1.0]),
            'similarity': 0.0,
        },
    ]

    for case in cases:
        output = analyze.cosine_similarity_vectors(case['v1'], case['v2'])
        
        # check output with small error margin
        assert round(output, 8) == case['similarity']

def test_cosine_similarity_matrix_vector():
    cases = [
        {
            'v': np.array([1.0, 1.0]),
            'M': np.array([[1.0, 0.0], [1.0, 0.0]]),
            'similarity': np.array([0.5, 0.5]),
        }
    ]

    for case in cases:
        output = analyze.cosine_similarity_vectors(case['v'], case['M'])
        
        # check output with small error margin
        assert np.all(np.round(output, 8) == case['similarity'])

