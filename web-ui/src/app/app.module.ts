import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { NgModule } from '@angular/core';
import { CommonModule, TitleCasePipe } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Http, HttpModule, XSRFStrategy, CookieXSRFStrategy } from '@angular/http';
import { RouterModule, Routes } from '@angular/router';

import { MarkdownModule } from 'ngx-md';
import { ButtonModule, CalendarModule, DropdownModule, MultiSelectModule, SliderModule, MenuModule, DialogModule, CheckboxModule, SharedModule, TabViewModule } from 'primeng/primeng';
import { TableModule } from 'primeng/table';
import { RestHandler, IRestRequest, IRestResponse } from 'rest-core';
import { RestHandlerHttp, RestModule } from 'rest-ngx-http';

import { ApiService, ApiRetryService, ConfigService, CorpusService, DataService, DownloadService, ElasticSearchService, HighlightService, ManualService, NotificationService, SearchService, SessionService, UserService, LogService, QueryService } from './services/index';

import { AppComponent } from './app.component';
import { CorpusSelectionComponent } from './corpus-selection/corpus-selection.component';
import { DropdownComponent } from './dropdown/dropdown.component';
import { HomeComponent } from './home/home.component';
import { HighlightPipe, SearchComponent, SearchFilterComponent, SearchRelevanceComponent, SearchResultsComponent, SearchSortingComponent } from './search/index';
import { ManualComponent } from './manual/manual.component';
import { ManualDialogComponent } from './manual/manual-dialog.component';
import { ManualNavigationComponent } from './manual/manual-navigation.component';
import { MenuComponent } from './menu/menu.component';
import { NotificationsComponent } from './notifications/notifications.component';
import { CorpusGuard } from './corpus.guard';
import { LoggedOnGuard } from './logged-on.guard';
import { LoginComponent } from './login/login.component';
import { BalloonDirective } from './balloon.directive';
import { ScrollToDirective } from './scroll-to.directive';
import { BarChartComponent } from './visualization/barchart.component';
import { TimelineComponent } from './visualization/timeline.component';
import { WordcloudComponent } from './visualization/wordcloud.component';
import { VisualizationComponent } from './visualization/visualization.component';
import { FreqtableComponent } from './visualization/freqtable.component';
import { DocumentViewComponent } from './document-view/document-view.component';
import { SearchHistoryComponent, HistoryQueryDisplayComponent } from './search-history/index';
import { SelectFieldComponent } from './search/select-field.component';
import { RegistrationComponent } from './registration/registration.component';
import { PrivacyComponent } from './privacy/privacy.component';

const appRoutes: Routes = [
    {
        path: 'search/:corpus',
        component: SearchComponent,
        canActivate: [CorpusGuard, LoggedOnGuard]
    },
    {
        path: 'login',
        component: LoginComponent
    },
    {
        path: 'login/:activated',
        component: LoginComponent
    },
    {
        path: 'registration',
        component: RegistrationComponent
    },
    {
        path: 'privacy',
        component: PrivacyComponent
    },
    {
        path: 'home',
        component: HomeComponent,
        canActivate: [LoggedOnGuard]
    },
    {
        path: 'manual/:identifier',
        component: ManualComponent
    },
    {
        path: 'search-history',
        component: SearchHistoryComponent
    },
    {
        path: '',
        redirectTo: 'home',
        pathMatch: 'full'
    }
]
@NgModule({
    declarations: [
        AppComponent,
        BalloonDirective,
        DropdownComponent,
        HomeComponent,
        CorpusSelectionComponent,
        HighlightPipe,
        SearchComponent,
        SearchFilterComponent,
        SearchRelevanceComponent,
        SearchResultsComponent,
        SearchSortingComponent,
        ManualComponent,
        ManualDialogComponent,
        ManualNavigationComponent,
        MenuComponent,
        NotificationsComponent,
        LoginComponent,
        ScrollToDirective,
        BarChartComponent,
        VisualizationComponent,
        WordcloudComponent,
        TimelineComponent,
        DocumentViewComponent,
        SearchHistoryComponent,
        HistoryQueryDisplayComponent,
        FreqtableComponent,
        SelectFieldComponent,
        RegistrationComponent,
        PrivacyComponent
    ],
    imports: [
        BrowserAnimationsModule,
        BrowserModule,
        CalendarModule,
        CommonModule,
        DropdownModule,
        FormsModule,
        HttpModule,
        RouterModule.forRoot(appRoutes),
        MarkdownModule,
        MultiSelectModule,
        SliderModule,
        MenuModule,
        DialogModule,
        CheckboxModule,
        SharedModule,
        TableModule,
        TabViewModule,
        RestModule.forRoot({
            handler: { provide: RestHandler, useFactory: (restHandlerFactory), deps: [Http] }
        })
    ],
    providers: [
        ApiService, 
        ApiRetryService, 
        CorpusService, 
        ConfigService, 
        DataService, 
        DownloadService, 
        ElasticSearchService, 
        HighlightService, 
        LogService, 
        ManualService, 
        NotificationService, 
        QueryService, 
        SearchService, 
        SessionService, 
        UserService, 
        CorpusGuard, 
        LoggedOnGuard, 
        TitleCasePipe,
        {
            provide: XSRFStrategy,
            useValue: new CookieXSRFStrategy('csrf_token', 'X-XSRF-Token')
        }],
    bootstrap: [AppComponent]
})
export class AppModule { }

// AoT requires an exported function for factories
export function restHandlerFactory(http: Http) {
    return new RestHandlerHttp(http);
}
