import { SearchFilter, SearchFilterData } from './search-filter';

// corresponds to the corpus definition on the backend.
export class Corpus implements ElasticSearchIndex {
    constructor(
        public serverName,
        /**
         * Internal name for referring to this corpus e.g. in URLs.
         */
        public name: string,
        /**
         * Human readable title of this corpus.
         */
        public title: string,
        /**
         * Description of the corpus to show to users.
         */
        public description: string,
        public doctype: DocumentType,
        public index: string,
        public fields: CorpusField[],
        public minDate: Date,
        public maxDate: Date,
        public image: string,
        public scan_image_type: string,
        public allow_image_download: boolean,
        public word_models_present: boolean,
        public descriptionpage?: string) { }

}

export type ElasticSearchIndex = {
    doctype: DocumentType,
    index: string,
    serverName: string
};

export type DocumentType = 'article';

export type CorpusField = {
    description: string,
    displayName: string,
    /**
     * How the field value should be displayed.
     * text_content: Main text content of the document
     */
    displayType: 'text_content' | 'px' | 'keyword' | 'integer' | 'text' | 'date' | 'boolean',
    resultsOverview?: boolean,
    csvCore?: boolean,
    searchFieldCore?: boolean,
    visualizations?: string[],
    visualizationSort?: string,
    multiFields?: string[],
    hidden: boolean,
    sortable: boolean,
    primarySort: boolean,
    searchable: boolean,
    downloadable: boolean,
    name: string,
    searchFilter: SearchFilter<SearchFilterData> | null,
};
