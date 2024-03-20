from typing import Dict, List
from datetime import datetime

from addcorpus.models import Corpus, CorpusConfiguration, Field
from addcorpus.json_corpora.utils import get_path, has_path

def import_json_corpus(data: Dict) -> Corpus:
    name = get_path(data, 'name')

    corpus, _created = Corpus.objects.get_or_create(name=name)

    configuration = import_configuration(data)
    configuration.corpus = corpus
    configuration.full_clean()
    configuration.save()

    return corpus

def import_configuration(data: Dict) -> CorpusConfiguration:
    title = get_path(data, 'meta', 'title')
    description = get_path(data, 'meta', 'description')
    category = get_path(data, 'meta', 'category')
    es_index = get_path(data, 'name')
    image = 'missing.png' # TODO: fix this
    languages = get_path(data, 'meta', 'languages')
    min_date = parse_date(get_path(data, 'meta', 'date_range', 'min'))
    max_date = parse_date(get_path(data, 'meta', 'date_range', 'max'))
    default_sort = get_path(data, 'options', 'default_sort') or {}
    language_field = get_path(data, 'options', 'language_field') or ''
    document_context = get_path(data, 'options', 'document_context') or {}
    return CorpusConfiguration(
        title=title,
        description=description,
        category=category,
        es_index=es_index,
        image=image,
        languages=languages,
        min_date=min_date,
        max_date=max_date,
        default_sort=default_sort,
        language_field=language_field,
        document_context=document_context,
    )

def parse_date(date: str):
    return datetime.strptime(date, '%Y-%m-%d').date()

