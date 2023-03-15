import { mockField2, mockFieldDate } from '../../mock-data/corpus';
import { EsQuery } from '../services';
import { Corpus, } from './corpus';
import { QueryModel } from './query';
import { EsSearchClause } from './elasticsearch';
import { DateFilter } from './search-filter';
import { convertToParamMap } from '@angular/router';

const corpus: Corpus = {
    name: 'mock-corpus',
    title: 'Mock Corpus',
    serverName: 'default',
    description: '',
    index: 'mock-corpus',
    minDate: new Date('1800-01-01'),
    maxDate: new Date('1900-01-01'),
    image: '',
    scan_image_type: null,
    allow_image_download: true,
    word_models_present: false,
    fields: [
        mockField2,
        mockFieldDate,
    ],
};

describe('QueryModel', () => {
    let query: QueryModel;

    beforeEach(() => {
        query = new QueryModel(corpus);
    });

    it('should create', () => {
        expect(query).toBeTruthy();
    });

    it('should convert to an elasticsearch query', () => {
        expect(query.toEsQuery()).toEqual({
            query: {
                match_all: {}
            }
        });

        query.setQueryText('test');

        expect(query.toEsQuery()).toEqual({
            query: {
                simple_query_string: {
                    query: 'test',
                    lenient: true,
                    default_operator: 'or',
                }
            }
        });
    });

    it('should formulate parameters', () => {
        expect(query.toRouteParam()).toEqual({
            query: null,
            fields: null,
            speech: null,
            date: null,
            sort: null,
            highlight: null
        });

        query.setQueryText('test');

        expect(query.toRouteParam()).toEqual({
            query: 'test',
            fields: null,
            speech: null,
            date: null,
            sort: null,
            highlight: null,
        });

        const filter = new DateFilter(mockFieldDate);
        filter.setToValue(new Date('Jan 1 1850'));

        query.addFilter(filter);

        expect(query.toRouteParam()).toEqual({
            query: 'test',
            fields: null,
            speech: null,
            date: '1850-01-01:1850-01-01',
            sort: null,
            highlight: null,
        });

        query.setQueryText('');
        query.removeFilter(filter);

        expect(query.toRouteParam()).toEqual({
            query: null,
            fields: null,
            speech: null,
            date: null,
            sort: null,
            highlight: null
        });
    });

    it('should set from parameters', () => {
        const params = convertToParamMap({
            query: 'test',
            date: '1850-01-01:1850-01-01',
        });

        query.setFromParams(params);
        expect(query.queryText).toEqual('test');
        expect(query.filters.length).toBe(1);
    });
});
