from datetime import datetime
from flask import current_app
import os
from glob import glob
import re
from bs4 import BeautifulSoup
import json

from addcorpus.corpus import Corpus, CSVCorpus, XMLCorpus
from addcorpus.extract import Constant, CSV, XML, Metadata
from corpora.parliament.parliament import Parliament
import corpora.parliament.utils.field_defaults as field_defaults
import corpora.parliament.utils.formatting as formatting
import corpora.parliament.utils.parlamint as parlamint

def in_date_range(corpus, start, end):
    start_date = start or corpus.min_date
    end_date = end or corpus.max_date

    return start_date <= corpus.max_date and end_date >= corpus.min_date

class ParliamentIrelandOld(CSVCorpus):
    '''
    Class for extracting 1919-2013 Irish debates.

    Only used for data extraction, use the `ParliamentIreland` class in the application.
    '''

    data_directory = current_app.config['PP_IRELAND_DATA']
    min_date = datetime(year=1919, month=1, day=1)
    max_date = datetime(year=2013, month=12, day=31)

    field_entry = 'speechID'
    delimiter = '\t'

    def sources(self, start, end):
        if in_date_range(self, start, end):
            min_year = start.year if start else self.min_date.year
            max_year = end.year if end else self.max_date.year
            for tsv_file in glob('{}/**/Dail_debates_1919-2013_*.tab'.format(self.data_directory), recursive=True):
                year = int(re.search(r'(\d{4}).tab$', tsv_file).group(1))
                if year >= min_year and year <= max_year:
                    metadata = {}
                    yield tsv_file, metadata
        else:
            return []

    country = field_defaults.country()
    country.extractor = Constant('Ireland')

    chamber = field_defaults.chamber()
    chamber.extractor = Constant('Dáil')

    date = field_defaults.date()
    date.extractor = CSV('date')

    party = field_defaults.party()
    party.extractor = CSV('party_name')

    party_id = field_defaults.party_id()
    party_id.extractor = CSV('partyID')

    speaker = field_defaults.speaker()
    speaker.extractor = CSV('member_name')

    speaker_id = field_defaults.speaker_id()
    speaker_id.extractor = CSV('memberID')

    speaker_constituency = field_defaults.speaker_constituency()
    speaker_constituency.extractor = CSV('const_name')

    speech = field_defaults.speech()
    speech.extractor = CSV(
        'speech',
        multiple=True,
        transform = '\n'.join,
    )

    speech_id = field_defaults.speech_id()
    speech_id.extractor = CSV('speechID')

    topic = field_defaults.topic()
    topic.extractor = CSV('title')

    sequence = field_defaults.sequence()
    sequence.extractor = CSV(
        'speechID',
        transform = formatting.extract_integer_value
    )

    source_archive = field_defaults.source_archive()
    source_archive.extractor = Constant('1919-2013')

    url = field_defaults.url()

    fields = [
        country,
        chamber,
        date,
        party, party_id,
        speaker, speaker_id, speaker_constituency,
        speech, speech_id,
        sequence,
        source_archive,
        topic,
        url,
    ]

def get_json_metadata(directory):
    files = os.listdir(directory)
    filename = next(f for f in files if f.endswith('.json'))
    path = os.path.join(directory, filename)
    with open(path) as json_file:
        data = json.load(json_file)

    return data

def get_file_metadata(json_data, filename):
    data = next(
        file_data for file_data in json_data
        if file_data['file'] == filename
    )

    chamber_data = data['house_uri']
    useful_data = {
        'url': data['xml_url'],
        'house': chamber_data['houseCode'],
        'debate_type': chamber_data['chamberType'],
        'committee': chamber_data['showAs'] if chamber_data.get('committeeCode', None) else None,
        'legislature': chamber_data['houseNo'],
    }

    return useful_data


def extract_people_data(soup):
    references = soup.find(['meta', 'identification', 'references'])
    people_nodes = references.find_all('TLCPerson')
    data = map(extract_person_data, people_nodes)
    return {
        id: person_data for id, person_data in data
    }

def extract_person_data(person_node):
    id = '#' + person_node['eId']
    name = person_node['showAs']
    return id, { 'name': name }

def extract_roles_data(soup):
    references = soup.find(['meta', 'identification', 'references'])
    return {}

def strip_and_join_paragraphs(paragraphs):
    '''Strip whitespace from each  paragraph and join into a single string'''

    stripped = map(str.strip, paragraphs)
    return '\n'.join(stripped)

def extract_number_from_id(id):
    match = re.search(r'\d+', id)
    if match:
        return int(match.group(0))

def find_topic_heading(speech_node):
    return speech_node.find_previous_sibling('heading')



class ParliamentIrelandNew(XMLCorpus):
    '''
    Class for extracting 2014-2020 Irish debates.

    Only used for data extraction, use the `ParliamentIreland` class in the application.
    '''

    data_directory = current_app.config['PP_IRELAND_DATA']
    min_date = datetime(year=2014, month=1, day=1)
    max_date = datetime(year=2020, month=12, day=31)

    tag_toplevel = 'debate'
    tag_entry = 'speech'

    def sources(self, start, end):
        if in_date_range(self, start, end):
            for root, _, files in os.walk(self.data_directory):
                xml_files = [f for f in files if f.endswith('.xml')]
                if any(xml_files):
                    json_metadata = get_json_metadata(root)
                    for filename in xml_files:
                        xml_file = os.path.join(root, filename)

                        with open(xml_file) as infile:
                            soup = BeautifulSoup(infile, features = 'xml')

                        metadata = {
                            **get_file_metadata(json_metadata, filename),
                            'roles': extract_roles_data(soup),
                            'persons': extract_people_data(soup),
                        }

                        yield xml_file, metadata
        else:
            return []

    country = field_defaults.country()
    country.extractor = Constant('Ireland')

    chamber = field_defaults.chamber()
    chamber.extractor = Metadata(
        'house'
    )

    date = field_defaults.date()
    date.extractor = XML(
        tag = 'docDate',
        attribute = 'date',
        recursive = True,
        toplevel = True,
    )

    party = field_defaults.party()
    party_id = field_defaults.party_id()

    speaker = field_defaults.speaker()
    speaker.extractor = parlamint.person_attribute_extractor(
        'name',
        id_attribute = 'by'
    )

    speaker_id = field_defaults.speaker_id()
    speaker_id.extractor = XML(attribute='by')

    speaker_constituency = field_defaults.speaker_constituency()

    speech = field_defaults.speech()
    speech.extractor = XML(
        'p',
        multiple = True,
        transform = strip_and_join_paragraphs,
    )

    speech_id = field_defaults.speech_id()

    topic = field_defaults.topic()
    topic.extractor = XML(
        transform_soup_func = find_topic_heading,
        extract_soup_func = lambda node : node.text,
    )

    sequence = field_defaults.sequence()
    sequence.extractor = XML(
        attribute = 'eId',
        transform = extract_number_from_id,
    )

    source_archive = field_defaults.source_archive()
    source_archive.extractor = Constant('2014-2020')

    url = field_defaults.url()
    url.extractor = Metadata('url')

    fields = [
        country,
        chamber,
        date,
        party, party_id,
        speaker, speaker_id, speaker_constituency,
        speech, speech_id,
        sequence,
        source_archive,
        topic,
        url,
    ]


class ParliamentIreland(Parliament, Corpus):
    '''
    Class for 1919-2020 Irish debates.
    '''

    title = 'People & Parliament (Ireland)'
    description = 'Speeches from the Dáil Éireann and Seanad Éireann'
    min_date = datetime(year=1919, month=1, day=1)
    max_date = datetime(year=2020, month=12, day=31)
    data_directory = current_app.config['PP_IRELAND_DATA']
    es_index = current_app.config['PP_IRELAND_INDEX']
    image = 'ireland.png'
    description_page = 'ireland.md'
    language = None # corpus uses multiple languages, so we will not be using language-specific analyzers
    es_settings = {'index': {'number_of_replicas': 0}} # do not include analyzers in es_settings

    @property
    def subcorpora(self):
        return [
            ParliamentIrelandOld(),
            ParliamentIrelandNew(),
        ]

    def sources(self, start, end):
        for i, subcorpus in enumerate(self.subcorpora):
            for source in subcorpus.sources(start, end):
                filename, metadata = source
                metadata['subcorpus'] = i
                yield filename, metadata

    def source2dicts(self, source):
        filename, metadata = source

        subcorpus_index = metadata['subcorpus']
        subcorpus = self.subcorpora[subcorpus_index]

        return subcorpus.source2dicts(source)

    country = field_defaults.country()
    chamber = field_defaults.chamber()
    date = field_defaults.date()
    party = field_defaults.party()
    party_id = field_defaults.party_id()
    speaker = field_defaults.speaker()
    speaker_id = field_defaults.speaker_id()
    speaker_constituency = field_defaults.speaker_constituency()
    speech = field_defaults.speech()
    speech_id = field_defaults.speech_id()
    topic = field_defaults.topic()
    sequence = field_defaults.sequence()
    source_archive = field_defaults.source_archive()
    url = field_defaults.url()

    fields = [
        country,
        chamber,
        date,
        party, party_id,
        speaker, speaker_id, speaker_constituency,
        speech, speech_id,
        sequence,
        source_archive,
        topic,
        url,
    ]
