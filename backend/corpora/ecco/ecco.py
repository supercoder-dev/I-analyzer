'''
Collect corpus-specific information, that is, data structures and file
locations.
'''
import logging
from pprint import pprint
import random
import re
import sys
from datetime import datetime, timedelta
from os.path import join, dirname, isfile, split, splitext
import os

from flask import current_app

from addcorpus.corpus import XMLCorpus, Field, consolidate_start_end_years, string_contains
from addcorpus import filters
from addcorpus.extract import Combined, Metadata, XML


# Source files ################################################################


class Ecco(XMLCorpus):
    title = "Eighteenth Century Collections Online"
    description = "Digital collection of books published in Great Britain during the 18th century."
    min_date = datetime(year=1700, month=1, day=1)
    max_date = datetime(year=1800, month=12, day=31)
    data_directory = current_app.config['ECCO_DATA']
    es_index = current_app.config['ECCO_ES_INDEX']
    es_doctype = current_app.config['ECCO_ES_DOCTYPE']
    es_settings = None
    image = current_app.config['ECCO_IMAGE']

    # tag_toplevel = 'text'
    # tag_entry = 'p'

    # # New data members
    # definition_pattern = re.compile(r'didl')
    # page_pattern = re.compile(r'.*_(\d+)_alto')
    # article_pattern = re.compile(r'.*_(\d+)_articletext')

    # filename_pattern = re.compile(r'[a-zA-z]+_(\d+)_(\d+)')

    # non_xml_msg = 'Skipping non-XML file {}'
    # non_match_msg = 'Skipping XML file with nonmatching name {}'

    # def sources(self, start=min_date, end=max_date):
    #     logger = logging.getLogger(__name__)
    #     consolidate_start_end_years(start, end, self.min_date, self.max_date)
    #     year_matcher = re.compile(r'[0-9]{4}')
    #     for directory, subdirs, filenames in os.walk(self.data_directory):
    #         _body, tail = split(directory)
    #         if tail.startswith("."):
    #             # don't go through directories from snapshots
    #             subdirs[:] = []
    #             continue
    #         elif year_matcher.match(tail) and (int(tail) > end.year or int(tail) < start.year):
    #             # don't walk further if the year is not within the limits specified by the user
    #             subdirs[:] = []
    #             continue
    #         definition_file = next((join(directory, filename) for filename in filenames if
    #                             self.definition_pattern.search(filename)), None)
    #         if not definition_file:
    #             continue
    #         meta_dict = self.metadata_from_xml(definition_file, tags=[
    #                 "title",
    #                 "date",
    #                 "publisher",
    #                 {"tag": "spatial", "save_as":"distribution"},
    #                 "source",
    #                 "issuenumber",
    #                 "language",
    #                 "isVersionOf",
    #                 "temporal",
    #                 {"tag": "spatial", "attribute": {'type': 'dcx:creation'}, "save_as":"pub_place"}
    #         ])
    #         logger.debug(meta_dict)
    #         for filename in filenames:
    #             if filename != '.DS_Store':
    #                 name, extension = splitext(filename)
    #                 full_path = join(directory, filename)
    #                 if extension != '.xml':
    #                     logger.debug(self.non_xml_msg.format(full_path))
    #                     continue
    #                 #def_match = self.definition_pattern.match(name)
    #                 article_match = self.article_pattern.match(name)
    #                 if article_match:
    #                     parts = name.split("_")
    #                     record_id = parts[1] + \
    #                       ":a" + parts[2]
    #                     meta_dict.update({
    #                         'external_file': definition_file,
    #                         'id': record_id
    #                     })
    #                     yield full_path, meta_dict

    # @property
    # def fields(self):
    #     return [Field(
    #         name="url",
    #         display_name="Delpher URL",
    #         description="Link to record on Delpher",
    #         extractor=XML(tag='identifier',
    #                               toplevel=True,
    #                               recursive=True,
    #                               multiple=False,
    #                               secondary_tag={
    #                                   'tag': 'recordIdentifier',
    #                                   'match': 'id'
    #                               },
    #                               external_file={
    #                                   'xml_tag_toplevel': 'DIDL',
    #                                   'xml_tag_entry': 'dcx'
    #                               }
    #         )
    #     ),
    #     Field(
    #         name='date',
    #         display_name='Date',
    #         description='Publication date.',
    #         es_mapping={'type': 'date', 'format': 'yyyy-MM-dd'},
    #         results_overview=True,
    #         csv_core=True,
    #         visualization_type='timeline',
    #         search_filter=filters.DateFilter(
    #             self.min_date,
    #             self.max_date,
    #             description=(
    #                 'Accept only articles with publication date in this range.'
    #             )
    #         ),
    #         extractor=Metadata('date')
    #     ),
    #     Field(
    #         name='ocr',
    #         display_name='OCR confidence',
    #         description='OCR confidence level.',
    #         es_mapping={'type': 'float'},
    #         search_filter=filters.RangeFilter(0, 100,
    #                                           description=(
    #                                               'Accept only articles for which the Opitical Character Recognition confidence '
    #                                               'indicator is in this range.'
    #                                           )
    #                                           ),
    #         extractor=XML(tag='OCRConfidencelevel',
    #             toplevel=True,
    #             recursive=True,
    #             external_file={
    #                 'xml_tag_toplevel': 'DIDL',
    #                 'xml_tag_entry': 'dcx'
    #             },
    #             transform=lambda x: float(x)*100
    #         ),
    #         sortable=True
    #     ),
    #     Field(
    #         name='newspaper_title',
    #         display_name='Newspaper title',
    #         description='Title of the newspaper',
    #         results_overview=True,
    #         search_field_core=True,
    #         es_mapping={'type': 'keyword'},
    #         visualization_type='term_frequency',
    #         search_filter=filters.MultipleChoiceFilter(
    #             description='Accept only articles in these newspapers.',
    #             options=self.papers
    #         ),
    #         extractor=Metadata('title')
    #     ),
    #     Field(
    #         name='version_of',
    #         display_name='Version of',
    #         description='The newspaper is a version of this newspaper.',
    #         es_mapping={'type': 'keyword'},
    #         extractor=Metadata('isVersionOf')
    #     ),
    #     Field(
    #         name='issue_number',
    #         display_name='Issue number',
    #         description='Issue number of the newspaper',
    #         csv_core=True,
    #         es_mapping={'type': 'integer'},
    #         extractor=Metadata('issuenumber')
    #     ),
    #     Field(
    #         name='category',
    #         display_name='Category',
    #         description='Whether the item is an article, advertisment, etc.',
    #         csv_core=True,
    #         es_mapping={'type': 'keyword'},
    #         extractor=XML(tag='subject',
    #                               toplevel=True,
    #                               recursive=True,
    #                               multiple=False,
    #                               secondary_tag={
    #                                   'tag': 'recordIdentifier',
    #                                   'match': 'id'
    #                               },
    #                               external_file={
    #                                   'xml_tag_toplevel': 'DIDL',
    #                                   'xml_tag_entry': 'dcx'
    #                               }
    #                               ),
    #         search_filter=filters.MultipleChoiceFilter(
    #             description='Accept only articles in these categories.',
    #             options=['test', 'options']
    #         ),
    #     ),
    #     Field(
    #         name='circulation',
    #         display_name='Circulation',
    #         description='The area in which the newspaper was distributed.',
    #         es_mapping={'type': 'keyword'},
    #         csv_core=True,
    #         extractor=Metadata('spatial'),
    #         search_filter=filters.MultipleChoiceFilter(
    #             description='Accept only articles appearing in specific areas.',
    #             options=self.distribution
    #         ),
    #     ),
    #     Field(
    #         name='publisher',
    #         display_name='Publisher',
    #         description='Publisher',
    #         search_field_core=True,
    #         extractor=Metadata('publisher')
    #     ),
    #     Field(
    #         name='language',
    #         display_name='Language',
    #         description='language',
    #         es_mapping={'type': 'keyword'},
    #         extractor=Metadata('language'),
    #         search_filter=filters.MultipleChoiceFilter(
    #             description='Accept only articles in this language.',
    #             options=['nl', 'fr'],
    #         ),
    #     ),
    #     Field(
    #         name='article_title',
    #         display_name='Article title',
    #         description='Article title',
    #         results_overview=True,
    #         search_field_core=True,
    #         extractor=XML(tag='title', flatten=True, toplevel=True)
    #     ),
    #     Field(
    #         name='id',
    #         display_name='ID',
    #         description='Unique identifier of the entry.',
    #         extractor=Metadata('id')
    #     ),
    #     Field(
    #         name='source',
    #         display_name='Source',
    #         description='Library or archive which keeps the hard copy of this newspaper.',
    #         es_mapping={'type': 'keyword'},
    #         extractor=Metadata('source')
    #     ),
    #     Field(
    #         name='pub_place',
    #         display_name='Publication Place',
    #         description='Where the newspaper was published',
    #         es_mapping={'type': 'keyword'},
    #         extractor=Metadata('pub_place')
    #     ),
    #     Field(
    #         name='temporal',
    #         display_name='Publication frequency',
    #         description='publication frequency of the newspaper.',
    #         results_overview=True,
    #         csv_core=True,
    #         es_mapping={'type': 'keyword'},
    #         visualization_type='term_frequency',
    #         search_filter=filters.MultipleChoiceFilter(
    #             description='Accept only articles in newspapers with this publication frequency.',
    #             options=['Dag', 'Week', 'Maand'],
    #         ),
    #         extractor=Metadata('temporal')
    #     ),
    #     Field(
    #         name='content',
    #         display_name='Content',
    #         display_type='text_content',
    #         description='Text content.',
    #         results_overview=True,
    #         search_field_core=True,
    #         extractor=XML(tag='p', multiple=True,
    #                               flatten=True, toplevel=True),
    #         visualization_type="word_cloud"
    #     ),
    # ]
