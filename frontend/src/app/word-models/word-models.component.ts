import { Component, DoCheck, ElementRef, HostListener, OnInit, ViewChild } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import {BehaviorSubject, combineLatest as combineLatest } from 'rxjs';
import { Corpus, User } from '../models';
import { CorpusService, UserService } from '../services';
import { WordmodelsService } from '../services/wordmodels.service';

@Component({
    selector: 'ia-word-models',
    templateUrl: './word-models.component.html',
    styleUrls: ['./word-models.component.scss']
})
export class WordModelsComponent implements DoCheck, OnInit {
    @ViewChild('searchSection', {static: false})
    public searchSection: ElementRef;
    public isScrolledDown: boolean;

    user: User;
    corpus: Corpus;
    modelDocumentation: any;

    queryText: string;
    asTable = false;
    palette: string[];

    activeQuery: string;

    tabIndex = new BehaviorSubject<'relatedwords'|'wordcontext'|'plaintext'>('relatedwords');

    tabs = {
        relatedwords: {
            title: 'Related words',
            manual: 'relatedwords',
            chartID: 'chart'
        },
        wordcontext: {
            title: 'Word context',
            manual: undefined,
            chartID: undefined,
        },
        plaintext: {
            title: 'Plain text',
            manual: undefined,
            chartID: undefined,
        }
    };

    childComponentLoading: boolean;
    isLoading: boolean;
    errorMessage: string;

    constructor(private corpusService: CorpusService,
                private userService: UserService,
                private wordModelsService: WordmodelsService,
                private router: Router) {
        this.tabIndex.subscribe(tab => {
            // reset error message when switching tabs
            this.errorMessage = undefined;
        });
    }


    ngDoCheck() {
        if (this.isLoading !== this.childComponentLoading ) {
            this.isLoading = this.childComponentLoading;
        }
    }


    async ngOnInit(): Promise<void> {
        this.user = await this.userService.getCurrentUser();
        this.corpusService.currentCorpus.subscribe(this.setCorpus.bind(this));
    }

    setCorpus(corpus: Corpus): void {
        if (corpus && (!this.corpus || this.corpus.name !== corpus.name)) {
            this.corpus = corpus;
            if (!this.corpus.word_models_present) {
                this.router.navigate(['search', this.corpus.name]);
            }
            this.getDocumentation();
        }
    }

    getDocumentation() {
        this.wordModelsService.getWordModelsDocumentation({corpus_name: this.corpus.name}).then(result => {
            this.modelDocumentation = result.documentation;
        });
    }

    submitQuery(): void {
        this.activeQuery = this.queryText;
    }

    onIsLoading(isLoading: boolean): void {
        this.childComponentLoading = isLoading;
    }

    setErrorMessage(event: {message: string}): void {
        this.errorMessage = event.message;
    }

    get currentTab(): any {
        return this.tabs[this.tabIndex.value];
    }

    get imageFileName(): string {
        if (this.tabIndex && this.corpus) {
            return `${this.currentTab.name}_${this.corpus.name}.png`;
        }
    }

    @HostListener('window:scroll', [])
    onWindowScroll() {
        // mark that the search results have been scrolled down and we should some border
        this.isScrolledDown = this.searchSection.nativeElement.getBoundingClientRect().y === 0;
    }

}
