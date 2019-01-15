import { Component, OnChanges, OnInit, Input, ViewChild, SimpleChanges } from '@angular/core';
import { Corpus, FoundDocument } from '../models/index';
import { HttpClient } from '@angular/common/http';
import { ScanImageService } from '../services';
import { PdfViewerComponent } from 'ng2-pdf-viewer';
import { JsonPipe } from '@angular/common';

@Component({
    selector: 'ia-pdf-view',
    templateUrl: './pdf-view.component.html',
    styleUrls: ['./pdf-view.component.scss']
})
export class PdfViewComponent implements OnChanges, OnInit {
    @ViewChild(PdfViewerComponent)

    private pdfComponent: PdfViewerComponent;

    @Input()
    public corpus: Corpus;

    @Input()
    public document: FoundDocument;

    @Input()
    public query: string;

    public pdfSrc: ArrayBuffer;

    public page: number = 3;

    public startPage: number;

    public totalPages: number;

    public isLoaded: boolean = false;

    public pageArray: number[];

    public pdfInfo: pdfInfo;

    get_pdf() {
        this.scanImageService.get_source_pdf(
            this.corpus.index,
            this.document.fieldValues.image_path,
            this.document.fieldValues.page - 1) //0-indexed
            .then(
                results => {
                    // this.pdfHeader = JSON.parse(results.headers.pdf_info).map(
                    //     item => 
                    // )
                    this.pdfInfo = <pdfHeader>JSON.parse(results.headers.pdf_info)
                    this.pdfSrc = results.body;
                })
    }

    afterLoadComplete(pdfData: any) {
        this.totalPages = pdfData.numPages;
        // this.pageArray = Array.from(Array(pdfData.numPages)).map((x, i) => i + 1);
        this.pageArray = this.pdfInfo.page_numbers
        this.isLoaded = true;
    }

    nextPage() {
        this.page++;
    }

    prevPage() {
        this.page--;
    }

    setPage(pageNr: number) {
        this.page = pageNr;
    }

    public textLayerRendered(e: CustomEvent, querytext: string) {
        this.pdfComponent.pdfFindController.executeCommand('find', {
            caseSensitive: false, findPrevious: true, highlightAll: true, phraseSearch: true,
            query: querytext
        });
    }

    constructor(private scanImageService: ScanImageService, private http: HttpClient) { }

    ngOnInit() {
        this.get_pdf();
    }

    ngOnChanges(changes: SimpleChanges) {
        if (changes.document.previousValue && changes.document.previousValue != changes.document.currentValue) {
            console.log('docChange')
            this.isLoaded = false;
            this.page = this.pdfInfo.initial_page_index;
            this.get_pdf();
        }
    }

}

interface pdfHeader {
    page_numbers: number[];
    initial_page_index: number;
}
