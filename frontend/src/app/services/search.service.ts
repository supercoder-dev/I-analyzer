import { Injectable } from '@angular/core';

import { ApiService } from './api.service';
import { ElasticSearchService } from './elastic-search.service';
import {
    Corpus, QueryModel, SearchResults,
    AggregateQueryFeedback
} from '../models/index';
import { PageResultsParameters } from '../models/page-results';
import { Aggregator } from '../models/aggregation';


@Injectable()
export class SearchService {
    constructor(
        private apiService: ApiService,
        private elasticSearchService: ElasticSearchService,
    ) {
        window['apiService'] = this.apiService;
    }

    /**
     * Load results for requested page
     */
    public async loadResults(
        queryModel: QueryModel,
        resultsParams: PageResultsParameters,
    ): Promise<SearchResults> {
        const results = await this.elasticSearchService.loadResults(
            queryModel,
            resultsParams,
        );
        return this.filterResultsFields(results, queryModel);
    }

    public async aggregateSearch(
        corpus: Corpus,
        queryModel: QueryModel,
        aggregators: Aggregator[],
    ): Promise<AggregateQueryFeedback> {
        return this.elasticSearchService.aggregateSearch(
            corpus,
            queryModel,
            aggregators
        );
    }

    /** filter search results for fields included in resultsOverview of the corpus */
    private filterResultsFields(results: SearchResults, queryModel: QueryModel): SearchResults {
        return {
            fields: queryModel.corpus.fields.filter((field) => field.resultsOverview),
            total: results.total,
            documents: results.documents,
        } as SearchResults;
    }
}
