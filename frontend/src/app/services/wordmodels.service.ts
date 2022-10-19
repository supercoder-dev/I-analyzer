import { Injectable } from '@angular/core';
import { IResourceAction, IResourceMethod, Resource, ResourceAction, ResourceHandler, ResourceParams, ResourceRequestMethod } from '@ngx-resource/core';

import { environment } from '../../environments/environment';
import { RelatedWordsResults, WordInModelResult, WordSimilarity } from '../models';

// workaround for https://github.com/angular/angular-cli/issues/2034
type ResourceMethod<IB, O> = IResourceMethod<IB, O>;

@Injectable()
@ResourceParams()
export class WordmodelsService extends Resource {
    private wordModelsUrl: string;

    constructor(restHandler: ResourceHandler) {
        super(restHandler);
    }

    @ResourceAction({
        method: ResourceRequestMethod.Post,
        path: '/get_related_words'
    })
    public relatedWordsRequest: ResourceMethod<
        { query_term: string, corpus_name: string },
        { success: false, message: string } | { success: true, data: RelatedWordsResults }>;

    @ResourceAction({
        method: ResourceRequestMethod.Post,
        path: '/get_related_words_time_interval'
    })
    public relatedWordsTimeIntervalRequest: ResourceMethod<
        { query_term: string, corpus_name: string, time: string },
        { success: false, message: string } | { success: true, data: WordSimilarity[] }>;

    @ResourceAction({
        method: ResourceRequestMethod.Get,
        path: '/get_similarity_over_time'
    })
    public wordSimilarityRequest: ResourceMethod<
        { term_1: string, term_2: string, corpus_name: string},
        { success: false, message: string } | { success: true, data: WordSimilarity[] }
    >

    @ResourceAction({
        method: ResourceRequestMethod.Get,
        path: '/get_word_in_model'
    })
    public wordInModelRequest: ResourceMethod<
        { query_term: string, corpus_name: string, },
        { success: boolean, message: string, result: WordInModelResult }>;

    @ResourceAction({
        method: ResourceRequestMethod.Get,
        path: '/get_wm_documentation'
    })
    public wordModelsDocumentationRequest: ResourceMethod<
        { corpus_name: string },
        { documentation: string }
    >;

    $getUrl(actionOptions: IResourceAction): string | Promise<string> {
        const urlPromise = super.$getUrl(actionOptions);
        this.wordModelsUrl = environment.wordModelsUrl;
        return Promise.all([this.wordModelsUrl, urlPromise]).then(([wordModelsUrl, url]) => `${wordModelsUrl}${url}`);
    }

    public async getRelatedWords(queryTerm: string, corpusName: string): Promise<RelatedWordsResults> {
        return this.relatedWordsRequest({'query_term': queryTerm, 'corpus_name': corpusName}).then( result => {
            return new Promise( (resolve, reject) => {
                if (result['success'] === true) {
                    resolve(result.data);
                } else {
                    reject({'message': result.message});
                }
            });
        });
    }

    public async getWordSimilarity(term1: string, term2: string, corpusName: string): Promise<WordSimilarity[]> {
        return this.wordSimilarityRequest({'term_1': term1, 'term_2': term2, 'corpus_name': corpusName})
            .then( result => {
            return new Promise( (resolve, reject) => {
                if (result['success'] === true) {
                    resolve(result.data);
                } else {
                    reject({'message': result.message});
                }
            });
        });
    }

    public async getRelatedWordsTimeInterval(
        queryTerm: string, corpusName: string, timeInterval: string
    ): Promise<WordSimilarity[]> {
        return this.relatedWordsTimeIntervalRequest(
            {'query_term': queryTerm, 'corpus_name': corpusName, 'time': timeInterval}
        ).then( result => {
            return new Promise( (resolve, reject) => {
                if (result['success'] === true) {
                    resolve(result['data']);
                } else {
                    reject({'message': result.message});
                }
            });
        });
    }

    wordInModel(term: string, corpusName: string): Promise<WordInModelResult> {
        return this.wordInModelRequest({
            query_term: term,
            corpus_name: corpusName,
        }).then(result => {
            return new Promise( (resolve, reject) => {
                if (result['success'] === true) {
                    resolve(result.result);
                } else {
                    reject({'message': result['message']});
                }
            });
        });
    }


}
