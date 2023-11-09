from copy import copy
from os.path import join

from django.conf import settings

from addcorpus.corpus import XMLCorpusDefinition
from addcorpus.extract import XML, Constant, HTML, ExternalFile, Combined
from corpora.peaceportal.peaceportal import PeacePortal, categorize_material, clean_newline_characters, clean_commentary, join_commentaries, get_text_in_language
from corpora.utils.exclude_fields import exclude_fields_without_extractor

class PeaceportalIIS(PeacePortal, XMLCorpusDefinition):
    data_directory = settings.PEACEPORTAL_IIS_DATA
    es_index = getattr(settings, 'PEACEPORTAL_IIS_ES_INDEX', 'peaceportal-iis')
    es_alias = settings.PEACEPORTAL_ALIAS

    def add_metadata(self, filename):
        external_file_folder = settings.PEACEPORTAL_IIS_TXT_DATA
        return  {
            'associated_file': join(external_file_folder, filename)
        }

    def __init__(self):
        super().__init__()
        self.external_file_folder = settings.PEACEPORTAL_IIS_TXT_DATA
        self.source_database.extractor = Constant(
            value='Inscriptions of Israel/Palestine (Brown University)'
        )

        self._id.extractor = XML(
            tag=['teiHeader', 'fileDesc', 'sourceDesc',
                 'msDesc', 'msIdentifier', 'idno'],
            multiple=False,
            toplevel=False,
            flatten=True,
            transform=lambda x: ''.join(x.lower().split())
        )

        self.url.extractor = HTML(
            tag=['teiHeader', 'fileDesc', 'sourceDesc',
                 'msDesc', 'msIdentifier', 'idno'],
            multiple=False,
            toplevel=False,
            flatten=True,
            transform=lambda x: 'https://library.brown.edu/iip/viewinscr/{}'.format(
                ''.join(x.lower().split()))
        )

        # quick and dirty for now: extract value for 'notBefore'
        self.year.extractor = XML(
            tag=['teiHeader', 'fileDesc', 'sourceDesc', 'msDesc',
                 'history', 'origin', 'date'],
            toplevel=False,
            attribute='notBefore'
        )

        self.not_before.extractor = XML(
            tag=['teiHeader', 'fileDesc', 'sourceDesc', 'msDesc',
                 'history', 'origin', 'date'],
            toplevel=False,
            attribute='notBefore'
        )

        self.not_after.extractor = XML(
            tag=['teiHeader', 'fileDesc', 'sourceDesc', 'msDesc',
                 'history', 'origin', 'date'],
            toplevel=False,
            attribute='notAfter',
        )

        self.transcription.extractor = ExternalFile(
            stream_handler=extract_transcript
        )

        self.transcription_english.extractor = HTML(
            tag=['div'],
            toplevel=True,
            multiple=False,
            flatten=True,
            attribute_filter={
                'attribute': 'type',
                'value': 'translation'
            },
            transform_soup_func=extract_paragraph,
            transform=lambda x: ' '.join(x.split()) if x else None
        )

        # is not present in IIS data
        # self.names.extractor = XML(
        #     tag=['teiHeader', 'profileDesc',
        #          'particDesc', 'listPerson', 'person'],
        #     flatten=True,
        #     multiple=True,
        #     toplevel=False,
        # )

        self.iconography.extractor = XML(
            tag=['teiHeader', 'fileDesc', 'sourceDesc',
                 'msDesc', 'physDesc', 'decoDesc', 'decoNote'],
            toplevel=False,
            multiple=True,
            flatten=True
        )

        # is not present in IIS data
        self.sex.extractor = Constant(
            value='Unknown'
        )

        self.country.extractor = Constant(
            value='Israel/Palestine'
        )

        self.region.extractor = XML(
            tag=['teiHeader', 'fileDesc', 'sourceDesc', 'msDesc',
                 'history', 'origin', 'placeName', 'region'],
            toplevel=False,
            flatten=True
        )

        self.settlement.extractor = XML(
            tag=['teiHeader', 'fileDesc', 'sourceDesc', 'msDesc',
                 'history', 'origin', 'placeName', 'settlement'],
            toplevel=False,
            flatten=True
        )

        self.location_details.extractor = Combined(
            XML(
                tag=['teiHeader', 'fileDesc', 'sourceDesc', 'msDesc',
                     'history', 'origin', 'placeName'],
                toplevel=False,
                flatten=True
            ),
            XML(
                tag=['teiHeader', 'fileDesc', 'sourceDesc', 'msDesc',
                     'history', 'origin', 'p'],
                toplevel=False,
                flatten=True
            ),
            XML(
                tag=['teiHeader', 'fileDesc', 'sourceDesc', 'msDesc',
                     'history', 'provenance'],
                toplevel=False,
                flatten=True
            )
        )

        self.material.extractor = XML(
            tag=['teiHeader', 'fileDesc', 'sourceDesc', 'msDesc', 'physDesc',
                 'objectDesc', 'supportDesc'],
            attribute='ana',
            toplevel=False,
            flatten=True,
            transform=lambda x: categorize_material(x)
        )

        self.material_details.extractor = XML(
            tag=['teiHeader', 'fileDesc', 'sourceDesc', 'msDesc', 'physDesc',
                 'objectDesc', 'supportDesc'],
            attribute='ana',
            toplevel=False,
            flatten=True
        )

        self.language.extractor = Combined(
            XML(
                tag=['teiHeader', 'fileDesc', 'sourceDesc', 'msDesc', 'msContents',
                     'textLang'],
                attribute='mainLang',
                toplevel=False,
                transform=lambda x: normalize_language(x)
            ),
            XML(
                tag=['teiHeader', 'fileDesc', 'sourceDesc', 'msDesc', 'msContents',
                     'textLang'],
                attribute='otherLangs',
                toplevel=False,
                transform=lambda x: normalize_language(x)
            )
        )

        self.comments.extractor = Combined(
            XML(
                tag=['text'],
                toplevel=False,
                multiple=False,
                flatten=True,
                transform_soup_func=extract_comments,
                transform=lambda x: clean_commentary(x) if x else None
            ),
            XML(
                tag=['teiHeader', 'fileDesc', 'sourceDesc', 'msDesc', 'physDesc',
                    'objectDesc', 'supportDesc', 'condition'],
                toplevel=False,
                transform_soup_func=extract_condition
            ),
            XML(
                tag=['teiHeader', 'fileDesc', 'sourceDesc', 'msDesc', 'physDesc',
                    'objectDesc', 'layoutDesc', 'layout', 'p'],
                toplevel=False,
                transform=lambda x: 'LAYOUT:\n{}\n\n'.format(clean_commentary(x)) if x else None
            ),
            XML(
                tag=['teiHeader', 'fileDesc', 'sourceDesc', 'msDesc', 'physDesc',
                    'objectDesc'],
                toplevel=False,
                attribute='ana',
                transform=lambda x: 'OBJECTTYPE:\n{}\n\n'.format(x[1:]) if x else None
            ),
            XML(
                tag=['teiHeader', 'fileDesc', 'sourceDesc', 'msDesc', 'physDesc',
                     'objectDesc', 'supportDesc', 'support', 'dimensions'],
                toplevel=False,
                transform_soup_func=extract_dimensions,
                transform=lambda x: 'DIMENSIONS:\n{}\n\n'.format(
                    x) if x else None
            ),
            XML(
                tag=['teiHeader', 'fileDesc', 'sourceDesc', 'msDesc', 'physDesc',
                     'objectDesc', 'supportDesc', 'support', 'p'],
                toplevel=False,
                flatten=True,
                transform=lambda x: 'SUPPORT:\n{}\n\n'.format(
                    clean_commentary(x)) if x else None
            ),
            XML(
                tag=['teiHeader', 'fileDesc', 'sourceDesc', 'msDesc', 'physDesc', 'handDesc', 'handNote'],
                toplevel=False,
                transform_soup_func=extract_handnotes
            ),
            transform=lambda x: join_commentaries(x)
        )

        self.bibliography.extractor = XML(
            tag=['teiHeader', 'fileDesc', 'sourceDesc', 'msDesc',
                 'msIdentifier', 'publications', 'publication'],
            toplevel=False,
            multiple=True
        )

        self.transcription_hebrew.extractor = Combined(
            self.transcription.extractor,
            Constant('he'),
            transform=lambda x: get_text_in_language(x)
        )

        self.transcription_latin.extractor = Combined(
            self.transcription.extractor,
            Constant('la'),
            transform=lambda x: get_text_in_language(x)
        )

        self.transcription_greek.extractor = Combined(
            self.transcription.extractor,
            Constant('el'),
            transform=lambda x: get_text_in_language(x)
        )

        self.fields = exclude_fields_without_extractor(self.fields)


def extract_transcript(filestream):
    text = filestream.read().strip()
    filestream.close()
    # remove the tabs and spaces inherited from xml
    text = clean_newline_characters(text)
    if text:
        text = text.replace('\t', '')
    return text


def extract_paragraph(soup):
    '''
    Extract first <p> element from `soup`, ignore the rest.
    Ideal for ignoring <h2> headers in the HTML versions of the body.
    '''
    if not soup:
        return
    return soup.find('p')


def extract_comments(soup):
    '''
    Helper function to extract the commentary from either <body> or <back> (siblings under <text>)
    '''
    if not soup:
        return
    commentary_div = soup.find('div', {'type': 'commentary'})
    return extract_paragraph(commentary_div)


def extract_attribute_and_child_p(soup, field_header):
    '''
    Extract value for 'ana' attribute from soup,
    as well as the text from a <p> child. Will be returned
    in a new soup, i.e. a single element with text content
    in the following format `textcontent (attrivubtevalue)`
    '''
    result = ''
    text = ''
    ana = None
    if 'ana' in soup.attrs:
        ana = soup['ana']
    p = extract_paragraph(soup)
    if p:
        text = p.get_text()
        if text:
            result = clean_commentary(text)
    if ana:
        result = '{} ({})'.format(result, ana)

    if result:
        cloned_soup = copy(soup)
        cloned_soup.clear()
        cloned_soup.string = '{}:\n{}\n\n'.format(field_header, result)
        return cloned_soup


def extract_condition(soup):
    return extract_attribute_and_child_p(soup, 'CONDITION')


def extract_handnotes(soup):
    if not soup: return
    return extract_attribute_and_child_p(soup, 'HANDNOTES')


def extract_dimensions(soup):
    result = ''
    height_elem = soup.find('height')
    if height_elem:
        height = height_elem.get_text()
        if height:
            result = "H: {} ".format(height)

    width_elem = soup.find('width')
    if width_elem:
        width = width_elem.get_text()
        if width:
            result = "{}W: {}".format(result, width)

    depth_elem = soup.find('depth')
    if depth_elem:
        depth = depth_elem.get_text()
        if depth:
            result = "{} D: {}".format(result, depth)

    cloned_soup = copy(soup)
    cloned_soup.clear()
    cloned_soup.string = result
    return cloned_soup


def normalize_language(text):
    if not text:
        return
    ltext = text.lower().strip()
    if ltext in ['grc']:
        return 'Greek'
    if ltext in ['he', 'heb']:
        return 'Hebrew'
    if ltext in ['arc']:
        return 'Aramaic'
    if ltext in ['la', 'latin']:
        return 'Latin'

    # excluded (for now):
    # revision history

    # MISSING (i.e. present in Epidat and Fiji)
    # person(s) - names (profileDesc is completely missing)
