import { Component, EventEmitter, Input, OnChanges, Output } from '@angular/core';

import { DialogService, SearchService } from '../services/index';
@Component({
    selector: 'ia-related-words',
    templateUrl: './related-words.component.html',
    styleUrls: ['./related-words.component.scss']
})
export class RelatedWordsComponent implements OnChanges {
    @Input() searchData: {
        labels: string[],
        datasets: {
            label: string,
            data: number[],
            fill?: boolean,
            borderColor?: string
        }[]
    };
    @Input() queryText: string;
    @Input() corpusName: string;
    public zoomedInData; // data requested when clicking on a time interval
    // colour-blind friendly colorPalette retrieved from colorbrewer2.org
    public colorPalette = ['#a6611a', '#dfc27d', '#80cdc1', '#018571', '#543005', '#bf812d', '#f6e8c3', '#c7eae5', '#35978f', '#003c30']
    public chartOptions = {
        elements: {
            line: {
                tension: 0, // disables bezier curves
            }
        },
        scales: {
            yAxes: [{
                scaleLabel: {
                    display: true,
                    labelString: 'Cosine similarity (SVD_PPMI)'
                }
            }],
            xAxes: [],
        }
    }
    private event: any;
    @Output('error')
    public errorEmitter = new EventEmitter<string>();

    constructor(private dialogService: DialogService, private searchService: SearchService) { }

    ngOnChanges() {
        this.searchData.datasets.map((d, index) => {
            d.fill = false;
            d.borderColor = this.colorPalette[index];
        })
        if (this.zoomedInData) {
            this.zoomTimeInterval(this.event);
        }
    }

    showRelatedWordsDocumentation() {
        this.dialogService.showManualPage('relatedwords');
    }

    zoomTimeInterval(event: any) {
        this.event = event;
        this.searchService.getRelatedWordsTimeInterval(
            this.queryText,
            this.corpusName,
            this.searchData.labels[event.element._index])
            .then(results => {
                this.zoomedInData = results['graphData'];
                this.zoomedInData.datasets
                    .sort((a, b) => { return b.data[0] - a.data[0] })
                    .map((d, index) => {
                        d.backgroundColor = this.colorPalette[index];
                    })
                // hide grid lines as we only have one data point on x axis
                this.chartOptions.scales.xAxes = [{
                    gridLines: {
                        display: false
                    }
                }];
            })
            .catch(error => {
                this.errorEmitter.emit(error['message']);
            })
    }

    zoomBack() {
        this.zoomedInData = null;
        this.chartOptions.scales.xAxes = [];
    }

}
