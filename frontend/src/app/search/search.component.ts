import { Component, ElementRef, OnInit, ViewChild, HostListener } from '@angular/core';
import { ActivatedRoute, Router, ParamMap } from '@angular/router';
import { Observable } from 'rxjs';
import "rxjs/add/operator/filter";
import "rxjs/add/observable/combineLatest";
import * as _ from "lodash";

import { Corpus, CorpusField, ResultOverview, SearchFilter, searchFilterDataFromParam, QueryModel, FoundDocument, User, SortEvent } from '../models/index';
import { CorpusService, DataService, DialogService, SearchService, UserService } from '../services/index';

@Component({
    selector: 'ia-search',
    templateUrl: './search.component.html',
    styleUrls: ['./search.component.scss']
})
export class SearchComponent implements OnInit {
    @ViewChild('searchSection')
    public searchSection: ElementRef;

    public isScrolledDown: boolean;

    public corpus: Corpus;

    /**
     * The filters have been modified.
     */
    public hasModifiedFilters: boolean = false;
    public isSearching: boolean;
    public hasSearched: boolean;
    /**
     * Whether the total number of hits exceeds the download limit.
     */
    public hasLimitedResults: boolean = false;
    /**
     * Whether a document has been selected to be shown.
     */
    public showDocument: boolean = false;
    /**
     * The document to view separately.
     */
    public viewDocument: FoundDocument;
    /**
     * Hide the filters by default, unless an existing search is opened containing filters.
     */
    public showFilters: boolean | undefined;
    public user: User;

    /**
     * The next two members facilitate a p-multiSelect in the template.
     */
    public availableSearchFields: CorpusField[];
    public selectedSearchFields: CorpusField[];
    public queryModel: QueryModel;
    /**
     * This is the query text currently entered in the interface.
     */
    public queryText: string;
    /**
     * This is the query text currently used for searching,
     * it might differ from what the user is currently typing in the query input field.
     */
    public searchQueryText: string;

    public sortAscending: boolean;
    public sortField: CorpusField | undefined;

    private resultsCount: number = 0;
    public tabIndex: number;
    public documentTabIndex: number;
    public searchBarHeight: number;

    private searchFilters: SearchFilter [] = [];
    private activeFilters: SearchFilter [] = [];

    constructor(private corpusService: CorpusService,
        private dataService: DataService,
        private searchService: SearchService,
        private userService: UserService,
        private dialogService: DialogService,
        private activatedRoute: ActivatedRoute,
        private router: Router) {
        }

    async ngOnInit() {
        this.user = await this.userService.getCurrentUser();
        Observable.combineLatest(
            this.corpusService.currentCorpus,
            this.activatedRoute.paramMap,
            (corpus, params) => {
                return { corpus, params };
            }).filter(({ corpus, params }) => !!corpus)
            .subscribe(({ corpus, params }) => {
                this.queryText = params.get('query');
                this.setCorpus(corpus);
                this.setFiltersFromParams(this.searchFilters, params);
                this.setSearchFieldsFromParams(params);
                this.setSortFromParams(this.corpus.fields, params);
                let queryModel = this.createQueryModel();
                if (this.queryModel !== queryModel) {
                    this.queryModel = queryModel;
                }
            });
    }

    @HostListener("window:scroll", [])
    onWindowScroll() {
        // mark that the search results have been scrolled down and we should some border
        this.isScrolledDown = this.searchSection.nativeElement.getBoundingClientRect().y == 0;
    }

    public changeSorting(event: SortEvent) {
        this.sortField = event.field;
        this.sortAscending = event.ascending;
        this.search();
    }

    public search() {
        this.queryModel = this.createQueryModel();
        let route = this.searchService.queryModelToRoute(this.queryModel);
        let url = this.router.serializeUrl(this.router.createUrlTree(
            ['.', route],
            { relativeTo: this.activatedRoute },
        ));
        if (this.router.url !== url) {
            this.router.navigateByUrl(url);
        }
    }

    /**
     * Event triggered from search-results.component
     * @param input
     */
    public onSearched(input: ResultOverview) {
        this.isSearching = false;
        this.hasSearched = true;
        this.resultsCount = input.resultsCount;
        this.searchQueryText = input.queryText;
        this.hasLimitedResults = this.user.downloadLimit && input.resultsCount > this.user.downloadLimit;
    }

    public onViewDocument(viewEvent: {document: FoundDocument, tabIndex?: number}) {
        this.showDocument = true;
        this.viewDocument = viewEvent.document;
        this.documentTabIndex = viewEvent.tabIndex;
    }

    public showQueryDocumentation() {
        this.dialogService.showManualPage('query');
    }

    public showCorpusInfo(corpus: Corpus) {
        this.dialogService.showDescriptionPage(corpus);
    }

    private getQueryFields(): string[] | null {
        let fields = this.selectedSearchFields.map(field => field.name);
        if (!fields.length) return null;
        return fields;
    }

    private createQueryModel() {
        return this.searchService.createQueryModel(this.queryText, this.getQueryFields(), this.activeFilters, this.sortField, this.sortAscending);
    }

    /**
     * Escape field names these so they won't interfere with any other parameter (e.g. query)
     */

    private setCorpus(corpus: Corpus) {
        if (!this.corpus || this.corpus.name != corpus.name) {
            this.corpus = corpus;
            this.availableSearchFields = Object.values(this.corpus.fields).filter(field => field.searchable);
            this.selectedSearchFields = [];
            this.queryModel = null;
        }
    }

    /**
     * Set the filter data from the query parameters and return whether any filters were actually set.
     */
    private setFiltersFromParams(searchFilters: SearchFilter[], params: ParamMap) {
        searchFilters.forEach( f => {
            let param = this.searchService.getParamForFieldName(f.fieldName);
            if (params.has(param)) {
                if (this.showFilters == undefined) {
                    this.showFilters = true;
                }
                let filterSettings = params.get(param).split(',');
                if (filterSettings[0] == "") filterSettings = [];
                f.currentData = searchFilterDataFromParam(f.fieldName, f.currentData.filterType, filterSettings);
                f.useAsFilter = true;
            }
            else {
                f.useAsFilter = false;
            }
        })
    }

    private setSearchFieldsFromParams(params: ParamMap) {
        if (params.has('fields')) {
            let queryRestriction = params.get('fields').split(',');
            this.selectedSearchFields = queryRestriction.map(
                fieldName => this.corpus.fields.find(
                    field => field.name === fieldName
                )
            );
        }
    }

    private setSortFromParams(corpusFields: CorpusField[], params: ParamMap) {
        if (params.has('sort')) {
            let [sortField, sortAscending] = params.get('sort').split(',');
            this.sortField = corpusFields.find(field => field.name == sortField);
            this.sortAscending = sortAscending == 'asc';
        } else {
            this.sortField = undefined;
        }
    }

    public setActiveFilters(activeFilters: SearchFilter[]) {
        this.activeFilters = activeFilters;
        this.search();
    }

    private tabChange(event) {
        this.tabIndex = event.index;
    }

    private selectSearchFields(selection: CorpusField[]) {
        this.selectedSearchFields = selection;
        this.search();
    }
}
