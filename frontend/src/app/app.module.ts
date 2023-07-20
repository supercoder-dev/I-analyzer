import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { NgModule, APP_INITIALIZER } from '@angular/core';
import { APP_BASE_HREF, TitleCasePipe } from '@angular/common';

import { HttpClient, HttpClientModule } from '@angular/common/http';
import { HttpClientXsrfModule } from '@angular/common/http';
import { RouterModule, Routes } from '@angular/router';

import { ChartModule } from 'primeng/chart';
import { DropdownModule } from 'primeng/dropdown';
import { MultiSelectModule } from 'primeng/multiselect';
import { SliderModule } from 'primeng/slider';
import { MenuModule } from 'primeng/menu';
import { DialogModule } from 'primeng/dialog';
import { ConfirmDialogModule } from 'primeng/confirmdialog';
import { ChipsModule } from 'primeng/chips';
import { TableModule } from 'primeng/table';
import { ResourceHandler } from '@ngx-resource/core';
import { ResourceHandlerHttpClient, ResourceModule } from '@ngx-resource/handler-ngx-http';
import { PdfViewerModule } from 'ng2-pdf-viewer';
import { CookieService } from 'ngx-cookie-service';

import { ApiService, ApiRetryService, CorpusService, DialogService, DownloadService,
    ElasticSearchService, HighlightService, NotificationService, SearchService, SessionService,
    UserService, QueryService } from './services/index';

import { AppComponent } from './app.component';
import { AboutComponent } from './about/about.component';
import { CorpusSelectionComponent } from './corpus-selection/corpus-selection.component';
import { HomeComponent } from './home/home.component';
import { SearchComponent, SearchRelevanceComponent, SearchResultsComponent, SearchSortingComponent } from './search/index';
import { ManualComponent } from './manual/manual.component';
import { ManualNavigationComponent } from './manual/manual-navigation.component';
import { MenuComponent } from './menu/menu.component';
import { NotificationsComponent } from './notifications/notifications.component';
import { CorpusGuard } from './corpus.guard';
import { LoggedOnGuard } from './logged-on.guard';
import { LoginComponent } from './login/login.component';
import { TimelineComponent } from './visualization/barchart/timeline.component';
import { WordcloudComponent } from './visualization/wordcloud/wordcloud.component';
import { VisualizationComponent } from './visualization/visualization.component';
import { FreqtableComponent } from './visualization/freqtable.component';
import { SearchHistoryComponent, QueryFiltersComponent, QueryTextPipe } from './history/search-history/index';
import { SelectFieldComponent } from './select-field/select-field.component';
import { RegistrationComponent } from './login/registration/registration.component';
import { PrivacyComponent } from './privacy/privacy.component';
import { RelatedWordsComponent } from './word-models/related-words/related-words.component';
import { DialogComponent } from './dialog/dialog.component';
import { DownloadComponent } from './download/download.component';
import { HistogramComponent } from './visualization/barchart/histogram.component';
import { ResetPasswordComponent } from './login/reset-password/reset-password.component';
import { RequestResetComponent } from './login/reset-password/request-reset.component';
import { PaginationComponent } from './search/pagination/pagination.component';
import { BooleanFilterComponent, FilterManagerComponent, MultipleChoiceFilterComponent,
    DateFilterComponent, RangeFilterComponent
} from './filter/index';
import { DocumentViewComponent } from './document-view/document-view.component';
import { ImageNavigationComponent, ImageViewComponent, ScanImageComponent, ScanPdfComponent } from './image-view';
import { NgramComponent } from './visualization/ngram/ngram.component';
import { BarchartOptionsComponent } from './visualization/barchart/barchart-options.component';
import { PaletteSelectComponent } from './visualization/visualization-footer/palette-select/palette-select.component';
import { AdHocFilterComponent } from './filter/ad-hoc-filter.component';
import { HighlightSelectorComponent } from './search/highlight-selector.component';
import { TimeIntervalSliderComponent } from './word-models/similarity-chart/time-interval-slider/time-interval-slider.component';
import { WordModelsComponent } from './word-models/word-models.component';
import { CorpusHeaderComponent } from './corpus-header/corpus-header.component';
import { VisualizationFooterComponent } from './visualization/visualization-footer/visualization-footer.component';
import { WordmodelsService } from './services/wordmodels.service';
import { QueryFeedbackComponent } from './word-models/query-feedback/query-feedback.component';
import { WordSimilarityComponent } from './word-models/word-similarity/word-similarity.component';
import { TermComparisonEditorComponent } from './visualization/barchart/term-comparison-editor/term-comparison-editor.component';
import { SimilarityChartComponent } from './word-models/similarity-chart/similarity-chart.component';
import { FullDataButtonComponent } from './visualization/full-data-button/full-data-button.component';
import { FooterComponent } from './footer/footer.component';
import { DownloadHistoryComponent } from './history/download-history/download-history.component';
import { HistoryDirective } from './history/history.directive';
import { DownloadOptionsComponent } from './download/download-options/download-options.component';
import { JoyplotComponent } from './visualization/ngram/joyplot/joyplot.component';
import { VerifyEmailComponent } from './login/verify-email/verify-email.component';
import { DocumentPageComponent } from './document-page/document-page.component';
import { CorpusSelectorComponent } from './corpus-selection/corpus-selector/corpus-selector.component';
import { CorpusFilterComponent } from './corpus-selection/corpus-filter/corpus-filter.component';
import { CorpusInfoComponent } from './corpus-info/corpus-info.component';
import { FieldInfoComponent } from './corpus-info/field-info/field-info.component';
import { SharedModule } from './shared/shared.module';


export const appRoutes: Routes = [
    {
        path: 'search/:corpus',
        component: SearchComponent,
        canActivate: [CorpusGuard, LoggedOnGuard],
    },
    {
        path: 'word-models/:corpus',
        component: WordModelsComponent,
        canActivate: [CorpusGuard, LoggedOnGuard],
    },
    {
        path: 'info/:corpus',
        component: CorpusInfoComponent,
        canActivate: [CorpusGuard, LoggedOnGuard]
    },
    {
        path: 'document/:corpus/:id',
        component: DocumentPageComponent,
        canActivate: [CorpusGuard, LoggedOnGuard],
    },
    {
        path: 'login',
        component: LoginComponent,
    },
    {
        path: 'login/:activated',
        component: LoginComponent,
    },
    {
        path: 'registration',
        component: RegistrationComponent,
    },
    {
        path: 'reset',
        component: RequestResetComponent,
    },
    {
        path: 'reset-password/:uid/:token',
        component: ResetPasswordComponent,
    },
    {
        path: 'privacy',
        component: PrivacyComponent,
    },
    {
        path: 'home',
        component: HomeComponent,
        canActivate: [LoggedOnGuard],
    },
    {
        path: 'manual/:identifier',
        component: ManualComponent,
    },
    {
        path: 'about',
        component: AboutComponent,
    },
    {
        path: 'search-history',
        component: SearchHistoryComponent,
    },
    {
        path: 'download-history',
        component: DownloadHistoryComponent,
    },
    {
        path: 'confirm-email/:key',
        component: VerifyEmailComponent,
    },
    {
        path: '',
        redirectTo: 'home',
        pathMatch: 'full',
    },
];

export const declarations: any[] = [
    AppComponent,
    AboutComponent,
    AdHocFilterComponent,
    BarchartOptionsComponent,
    BooleanFilterComponent,
    CorpusFilterComponent,
    CorpusHeaderComponent,
    CorpusInfoComponent,
    CorpusSelectionComponent,
    CorpusSelectorComponent,
    DateFilterComponent,
    DialogComponent,
    DocumentPageComponent,
    DocumentViewComponent,
    DownloadComponent,
    DownloadHistoryComponent,
    DownloadOptionsComponent,
    FilterManagerComponent,
    FieldInfoComponent,
    FooterComponent,
    FreqtableComponent,
    FullDataButtonComponent,
    HistoryDirective,
    HomeComponent,
    HistogramComponent,
    HighlightSelectorComponent,
    ImageViewComponent,
    ImageNavigationComponent,
    JoyplotComponent,
    LoginComponent,
    ManualComponent,
    ManualNavigationComponent,
    MenuComponent,
    MultipleChoiceFilterComponent,
    NgramComponent,
    NotificationsComponent,
    QueryFiltersComponent,
    QueryTextPipe,
    PaginationComponent,
    PaletteSelectComponent,
    PrivacyComponent,
    QueryFeedbackComponent,
    RangeFilterComponent,
    RegistrationComponent,
    RelatedWordsComponent,
    ResetPasswordComponent,
    RequestResetComponent,
    ScanImageComponent,
    ScanPdfComponent,
    SearchComponent,
    SearchHistoryComponent,
    SearchRelevanceComponent,
    SearchResultsComponent,
    SearchSortingComponent,
    SelectFieldComponent,
    SimilarityChartComponent,
    TermComparisonEditorComponent,
    TimeIntervalSliderComponent,
    TimelineComponent,
    VerifyEmailComponent,
    VisualizationComponent,
    VisualizationFooterComponent,
    WordcloudComponent,
    WordModelsComponent,
    WordSimilarityComponent,
];

// AoT requires an exported function for factories
export const resourceHandlerFactory = (http: HttpClient) =>
    new ResourceHandlerHttpClient(http);

export const imports: any[] = [
    BrowserAnimationsModule,
    BrowserModule,
    ChartModule,
    ChipsModule,
    ConfirmDialogModule,
    DialogModule,
    DropdownModule,
    HttpClientModule,
    HttpClientXsrfModule.withOptions({
        cookieName: 'csrftoken',
        headerName: 'X-CSRFToken',
    }),
    MenuModule,
    MultiSelectModule,
    PdfViewerModule,
    ResourceModule.forRoot({
        handler: {
            provide: ResourceHandler,
            useFactory: resourceHandlerFactory,
            deps: [HttpClient],
        },
    }),
    RouterModule.forRoot(appRoutes, { relativeLinkResolution: 'legacy' }),
    SharedModule,
    SliderModule,
    TableModule,
];

export const providers: any[] = [
    ApiService,
    ApiRetryService,
    CorpusService,
    DialogService,
    DownloadService,
    ElasticSearchService,
    HighlightService,
    NotificationService,
    QueryService,
    SearchService,
    SessionService,
    UserService,
    CorpusGuard,
    LoggedOnGuard,
    TitleCasePipe,
    CookieService,
    WordmodelsService,
    { provide: APP_BASE_HREF, useValue: '/' },
];

@NgModule({
    declarations,
    imports,
    providers,
    bootstrap: [AppComponent],
})
export class AppModule {}

