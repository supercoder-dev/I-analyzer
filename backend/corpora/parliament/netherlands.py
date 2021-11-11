from glob import glob
import logging

from flask import current_app

import bs4
from addcorpus.corpus import XMLCorpus
from addcorpus.extract import XML, Constant, Combined
from corpora.parliament.parliament import Parliament

import re

class ParliamentNetherlands(Parliament, XMLCorpus):
    '''
    Class for indexing Dutch parliamentary data
    '''

    title = "People & Parliament (Netherlands)"
    description = "Speeches from the Senate and House of Representatives"
    data_directory = current_app.config['PP_NL_DATA']
    es_index = current_app.config['PP_NL_INDEX']
    es_alias = current_app.config['PP_ALIAS']
    image = current_app.config['PP_NL_IMAGE']
    tag_toplevel = 'root'
    tag_entry = 'speech'


    def sources(self, start, end):
        logger = logging.getLogger(__name__)
        for xml_file in glob('{}/**/*.xml'.format(self.data_directory)):
            period_match = re.search(r'[0-9]{8}', xml_file)
            if period_match:
                period = period_match.group(0)
                start_year = int(period[:4])
                end_year = int(period[4:])

                if end_year >= start.year and start_year <= end.year:
                    yield xml_file
            else:
                yield xml_file
    
    def format_role(role):
        if role == 'mp':
            return role.upper()
        else:
            return role.title() if type(role) == str else role

    def find_topic(speech):
        return speech.find_parent('topic')
    
    def format_house(house):
        if house == 'senate':
            return 'Eerste Kamer'
        if house == 'commons':
            return 'Tweede Kamer'
        if house == 'other':
            return 'Other'
        return house
    
    def find_last_pagebreak(node):
        "find the last pagebreak node before the start of the current node"
        is_tag = lambda x : type(x) == bs4.element.Tag

        #look for pagebreaks in previous nodes
        for prev_node in node.previous_siblings:          
            if is_tag(prev_node):
                breaks = prev_node.find_all('pagebreak')
                if breaks:
                    return breaks[-1]
        
        #if none was found, go up a level
        parent = node.parent
        if parent:
            return ParliamentNetherlands.find_last_pagebreak(parent)
    
    def format_pages(pages):
        topic_start, topic_end, prev_break, last_break = pages
        if prev_break:
            if last_break:
                return '{}-{}'.format(prev_break, last_break)
            return str(prev_break)
        
        if topic_start and topic_end:
            return '{}-{}'.format(topic_start, topic_end)
    
    def format_party(data):
        name, id = data
        if name:
            return name
        if id and id.startswith('nl.p.'):
            id = id[5:]
        return id

    def __init__(self):
        self.country.extractor = Constant(
            value='Netherlands'
        )

        self.country.search_filter = None

        self.date.extractor = XML(
            tag=['meta','dc:date'],
            toplevel=True
        )

        self.house.extractor = XML(
            tag=['meta','dc:subject', 'pm:house'],
            attribute='pm:house',
            toplevel=True,
            transform=ParliamentNetherlands.format_house
        )

        self.debate_title.extractor = XML(
            tag=['meta', 'dc:title'],
            toplevel=True,
        )

        self.debate_id.extractor = XML(
            tag=['meta', 'dc:identifier'],
            toplevel=True,
        )

        self.topic.extractor = XML(
            transform_soup_func = ParliamentNetherlands.find_topic,
            attribute=':title',
        )

        self.speech.extractor = XML(
            tag='p',
            multiple=True,
            flatten=True,
        )

        self.speech_id.extractor = XML(
            attribute=':id'
        )

        self.speech.es_mapping = {
            "type" : "text",
            "analyzer": "dutch",
            "term_vector": "with_positions_offsets",
            "fields": {
                "exact": {
                    "type": "text",
                    "analyzer": "standard"
                    }
                }
            }

        self.speaker.extractor = Combined(
            XML(attribute=':function'),
            XML(attribute=':speaker'),
            transform=lambda x: ' '.join(x)
        )

        self.speaker_id.extractor = XML(
            attribute=':member-ref'
        )

        self.role.extractor = XML(
            attribute=':role',
            transform=ParliamentNetherlands.format_role
        )

        self.party.extractor = Combined(
            XML(
                attribute=':party'
                ),
            XML(
                attribute=':party-ref'
            ),
            transform=ParliamentNetherlands.format_party,
        )

        self.party_id.extractor = XML(
            attribute=':party-ref'
        )

        self.page.extractor = Combined(
            XML(transform_soup_func=ParliamentNetherlands.find_topic,
                attribute=':source-start-page'
            ),
            XML(transform_soup_func=ParliamentNetherlands.find_topic,
                attribute=':source-end-page'
            ),
            XML(transform_soup_func=ParliamentNetherlands.find_last_pagebreak,
                attribute=':originalpagenr',
            ),
            XML(tag=['stage-direction', 'pagebreak'],
                attribute=':originalpagenr',
                multiple=True,
                transform=lambda pages : pages[-1] if pages else pages
            ),
            transform=ParliamentNetherlands.format_pages,
        )
