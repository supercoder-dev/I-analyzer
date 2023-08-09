'''
Collect corpus-specific information, that is, data structures and file
locations.
'''

import logging
logger = logging.getLogger(__name__)
import os
from os.path import join, splitext
from datetime import datetime
import re

from django.conf import settings

from addcorpus import extract
from addcorpus import filters
from addcorpus.corpus import XMLCorpusDefinition, FieldDefinition

from addcorpus.es_mappings import keyword_mapping, main_content_mapping
from addcorpus.es_settings import es_settings


# Source files ################################################################


class Spectators(XMLCorpusDefinition):
    title = "Spectators"
    description = "A collection of Spectator newspapers"
    min_date = datetime()
    max_date = datetime()
    data_directory = settings.SPECTATORS_DATA
    es_index = getattr(settings, 'SPECTATORS_ES_INDEX', 'spectators')
    languages = ['en']

    tag_toplevel = 'article'
    tag_entry = 'content'

    # New data members
    filename_pattern = re.compile('[a-zA-z]+_(\d+)_(\d+)')
    non_xml_msg = 'Skipping non-XML file {}'
    non_match_msg = 'Skipping XML file with nonmatching name {}'

    @property
    def es_settings(self):
        return es_settings(self.languages[0], stopword_analyzer=True, stemming_analyzer=True)

    def sources(self, start=min_date, end=max_date):
        for directory, _, filenames in os.walk(self.data_directory):
            for filename in filenames:
                name, extension = splitext(filename)
                full_path = join(directory, filename)
                if extension != '.xml':
                    logger.debug(self.non_xml_msg.format(full_path))
                    continue
                match = self.filename_pattern.match(name)
                if not match:
                    logger.warning(self.non_match_msg.format(full_path))
                    continue

                issue, year = match.groups()
                if int(year) < start.year or end.year < int(year):
                    continue
                yield full_path, {
                    'year': year,
                    'issue': issue
                }

    overview_fields = ['magazine', 'issue', 'date', 'title', 'editor']

    fields = [
        FieldDefinition(
            name='date',
            display_name='Date',
            description='Publication date.',
            es_mapping={'type': 'date', 'format': 'yyyy-MM-dd'},
            histogram=True,
            results_overview=True,
            search_filter=filters.DateFilter(
                min_date,
                max_date,
                description=(
                    'Accept only articles with publication date in this range.'
                )
            ),
            extractor=extract.XML(tag='date', toplevel=True),
            csv_core=True
        ),
        FieldDefinition(
            name='id',
            display_name='ID',
            description='Unique identifier of the entry.',
            es_mapping=keyword_mapping(),
            extractor=extract.Combined(
                extract.XML(tag='magazine', toplevel=True),
                extract.Metadata('year'),
                extract.Metadata('issue'),
                transform=lambda x: '_'.join(x),
            ),
        ),
        FieldDefinition(
            name='issue',
            display_name='Issue number',
            es_mapping={'type': 'integer'},
            description='Source issue number.',
            results_overview=True,
            extractor=extract.XML(tag='issue', toplevel=True),
            csv_core=True,
        ),
        FieldDefinition(
            name='magazine',
            display_name='Magazine name',
            histogram=True,
            results_overview=True,
            es_mapping={'type': 'keyword'},
            description='Magazine name.',
            search_filter=filters.MultipleChoiceFilter(
                description='Search only within these magazines.',
                options=sorted(['De Hollandsche Spectator', 'De Denker']),
            ),
            extractor=extract.XML(tag='magazine', toplevel=True),
            csv_core=True
        ),
        FieldDefinition(
            name='editors',
            display_name='Editors',
            es_mapping=keyword_mapping(),
            description='Magazine editor(s).',
            extractor=extract.XML(tag='editor', toplevel=True, multiple=True)
        ),
        FieldDefinition(
            name='title',
            display_name='Title',
            results_overview=True,
            description='Article title.',
            extractor=extract.XML(tag='title', toplevel=True),
            search_field_core=True
        ),
        FieldDefinition(
            name='content',
            display_name='Content',
            display_type='text_content',
            description='Text content.',
            es_mapping=main_content_mapping(True, True, True),
            results_overview=True,
            extractor=extract.XML(tag='text', multiple=True, flatten=True),
            search_field_core=True
        ),
    ]

    document_context = {
        'context_fields': ['issue'],
        'sort_field': None,
        'sort_direction':  None,
        'context_display_name': 'issue'
    }
