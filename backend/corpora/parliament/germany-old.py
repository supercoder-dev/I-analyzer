from glob import glob
import logging

from flask import current_app

from corpora.parliament.parliament import Parliament
from addcorpus.extract import Constant, Combined, CSV
from addcorpus.corpus import CSVCorpus
from addcorpus.filters import MultipleChoiceFilter
import corpora.parliament.utils.field_defaults as field_defaults


class ParliamentGermanyOld(Parliament, CSVCorpus):
    title = 'People & Parliament (Germany Reichstag - 1867-1942)'
    description = "Speeches from the Reichstag"
    data_directory = current_app.config['PP_GERMANY_OLD_DATA']
    es_index = current_app.config['PP_GERMANY_OLD_INDEX']
    image = current_app.config['PP_GERMANY_OLD_IMAGE']
    es_settings = current_app.config['PP_ES_SETTINGS']
    es_settings['analysis']['filter'] = {
        "stopwords": {
          "type": "stop",
          "stopwords": "_german_"
        },
        "stemmer": {
            "type": "stemmer",
            "language": "german"
        }
    }

    def standardize_bool(date_is_estimate):
        return date_is_estimate.lower()

    field_entry = 'item_order'
    required_field = 'text'

    country = field_defaults.country()
    country.extractor = Constant(
        value='Germany'
    )

    country.search_filter = None

    book_id = field_defaults.book_id()
    book_id.extractor = CSV(
        field='book_id'
    )

    book_label = field_defaults.book_label()
    book_label.extractor = CSV(
        field='book_label'
    )

    parliament = field_defaults.parliament()
    parliament.extractor = CSV(
        field='parliament'
    )

    date = field_defaults.date()
    date.extractor = CSV(
        field='date'
    )

    date_is_estimate = field_defaults.date_is_estimate()
    date_is_estimate.extractor = CSV(
        field='date_is_estimate',
        transform=standardize_bool
    )

    session = field_defaults.session()
    session.extractor = CSV(
        field='sitzung'
    )

    page = field_defaults.page()
    page.extractor = CSV(
        field='page_number'
    )

    speech = field_defaults.speech()
    speech.extractor = CSV(
        field='text',
        multiple=True,
        transform=lambda x : ' '.join(x)
    )
    
    source_url = field_defaults.source_url()
    source_url.extractor = CSV(
        field='img_url'
    )

    speech_id = field_defaults.speech_id()
    speech_id.extractor = CSV(
        field='item_order'
    )

    def __init__(self):
        self.fields = [
            self.country,
            self.book_id, self.book_label,
            self.parliament, 
            self.date, self.date_is_estimate,
            self.session, 
            self.page, self.source_url,
            self.speech, self.speech_id,
        ]