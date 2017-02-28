'''
This module is a tool to define how to extract specific information from an
object such as a dictionary or a BeautifulSoup XML node. 
'''

import logging; logger = logging.getLogger(__name__)
import re
import html
import bs4


class Extractor(object):
    '''
    An extractor contains a method that can be applied to some number arguments
    and attempts to obtain from that the information that it was looking for.
    '''
    
    def __init__(self,
        applicable=None, # Predicate that takes metadata and decides whether
                         # this extractor is applicable. None means always.
        transform=None   # Optional function to postprocess extracted value
        ):
        self.transform = transform
        self.applicable = applicable 



    def apply(self, *nargs, **kwargs):
        '''
        Test if the extractor is applicable to the given arguments and if so,
        try to extract the information. 
        '''
        if self.applicable is None or self.applicable(kwargs.get('metadata')):
            result = self._apply(*nargs, **kwargs)

            try:
                if self.transform:
                    return self.transform(result)
            except Exception:
                logging.critical("Value {v} could not be converted."\
                    .format(v=result, k=key))
                return None
            else:
                return result
        else:
            return None


    def _apply(self, *nargs, **kwargs):
        '''
        Actual extractor method to be implemented in subclasses (assume that
        testing for applicability and post-processing is taken care of).
        '''
        raise NotImplementedError()



class Choice(Extractor):
    '''
    Use the first applicable extractor from a list of extractors.
    '''
    
    def __init__(self, *nargs, **kwargs):
        self.extractors = list(nargs)
        super().__init__(**kwargs)
        
        
        
    def _apply(self, metadata, *nargs, **kwargs):
        for extractor in self.extractors:
            if extractor.applicable is None or extractor.applicable(metadata):
                return extractor.apply(metadata=metadata, *nargs, **kwargs)
        return None



class Constant(Extractor):
    '''
    This extractor 'extracts' the same value every time, regardless of input.
    '''
    
    def __init__(self, value, *nargs, **kwargs):
        self.value = value
        super().__init__(*nargs, **kwargs)
    
    
    def _apply(self, *nargs, **kwargs):
        return self.value
        
        


class Metadata(Extractor):
    '''
    This extractor extracts a value from provided metadata.
    '''
    
    
    def __init__(self, key, *nargs, **kwargs):
        self.key = key
        super().__init__(*nargs, **kwargs)
        
    
    
    def _apply(self, metadata, *nargs, **kwargs):
        return metadata.get(self.key)




class XML(Extractor):
    '''
    This extractor extracts attributes or contents from a BeautifulSoup node.
    '''

    def __init__(self,
        tag=[], # Tag to select. When this is a list, read as a path (e.g.
                # select successive children; makes sense when recursive=False)
        attribute=None, # Which attribute, if any, to select
        flatten=False, # Flatten the text content of a non-text children?
        toplevel=False, # Tag to select for search: top-level or entry tag
        recursive=False, # Whether to search all descendants
        multiple=False, # Whether to abandon the search after the first element
        *nargs,
        **kwargs
        ):
        
        self.tag = tag
        self.attribute = attribute
        self.flatten = flatten
        self.toplevel = toplevel
        self.recursive = recursive
        self.multiple = multiple
        super().__init__(*nargs, **kwargs)



    def _select(self, soup):
        '''
        Return the BeautifulSoup element that matches the constraints of this
        extractor.
        '''
        # If the tag was a path, walk through it before continuing
        tag = self.tag
        if isinstance(self.tag, list):
            for i in range(0, len(self.tag)-1):
                if self.tag[i] == '..':
                    soup = soup.parent
                elif self.tag[i] == '.':
                    pass
                else:
                    soup = soup.find(self.tag[i], recursive=self.recursive)
                if not soup:
                    return None
            tag = self.tag[-1]

        # Find and return (all) relevant BeautifulSoup element(s)
        if self.multiple:
            return soup.find_all(tag, recursive=self.recursive)
        else:
            return soup.find(tag, recursive=self.recursive)



    def _apply(self, soup_top, soup_entry, *nargs, **kwargs):
        
        # Select appropriate BeautifulSoup element
        soup = self._select(soup_top if self.toplevel else soup_entry)

        if not soup:
            return None

        # Use appropriate extractor
        if self.attribute:
            return self._attr(soup)
        else:
            if self.flatten:
                return self._flatten(soup)
            else:
                return self._string(soup)



    def _string(self, soup):
        '''
        Output direct text contents of a node.
        '''

        if isinstance(soup, bs4.element.Tag):
            return soup.string
        else:
            return [ node.string for node in soup ]



  
    def _flatten(self, soup):
        '''
        Output text content of node and descendant nodes, disregarding
        underlying XML structure.
        '''

        if isinstance(soup, bs4.element.Tag):
            text = soup.get_text()
        else:
            text = '\n\n'.join(node.get_text() for node in soup)

        _softbreak = re.compile('(?<=\S)\n(?=\S)| +')
        _newlines  = re.compile('\n+')

        return html.unescape(
            _newlines.sub('\n',
                _softbreak.sub(' ', text)
            ).strip()
        )



    def _attr(self, soup):
        '''
        Output content of nodes' attribute.
        '''

        if isinstance(soup, bs4.element.Tag):
            return soup.attrs.get(self.attribute)
        else:
            return [
                node.attrs.get(self.attr)
                for node in soup if node.attrs.get(self.attribute) is not None
            ]
