import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { faBookOpen } from '@fortawesome/free-solid-svg-icons';
import * as _ from 'lodash';
import { combineLatest } from 'rxjs';
import { Corpus, FoundDocument } from '../models';
import { CorpusService, ElasticSearchService } from '../services';
import { makeContextParams } from '../utils/document-context';

@Component({
  selector: 'ia-document-page',
  templateUrl: './document-page.component.html',
  styleUrls: ['./document-page.component.scss']
})
export class DocumentPageComponent implements OnInit {
    corpus: Corpus;
    documentId: string;
    document: FoundDocument;

    documentNotFound: boolean;

    contextIcon = faBookOpen;

    constructor(
        private corpusService: CorpusService,
        private elasticSearchService: ElasticSearchService,
        private activatedRoute: ActivatedRoute,
    ) { }

    get contextDisplayName(): string {
        if (this.document?.hasContext) {
            return this.corpus.documentContext.displayName;
        }
    }

    get contextLink(): any {
        if (this.document && this.corpus) {
            return ['/search', this.corpus.name];
        }
    }

    get contextQueryParams(): any {
        if (this.document && this.corpus) {
            return makeContextParams(this.document, this.corpus);
        }
    }

    ngOnInit(): void {
        combineLatest([
            this.activatedRoute.params,
            this.corpusService.currentCorpus
        ]).subscribe(([params, corpus]) => {
            this.corpus = corpus;
            this.documentId = params['id'];
            this.getDocument(this.documentId);
        });
    }

    getDocument(id: string) {
        this.elasticSearchService.getDocumentById(id, this.corpus).then(document => {
            this.document = document;
            this.documentNotFound = _.isUndefined(this.document);
        });
    }


}
