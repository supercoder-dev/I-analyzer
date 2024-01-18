import { Component, Input } from '@angular/core';
import { actionIcons } from '../shared/icons';
import { PageResults } from '../models/page-results';
import { Observable } from 'rxjs';


@Component({
  selector: 'ia-highlight-selector',
  templateUrl: './highlight-selector.component.html',
  styleUrls: ['./highlight-selector.component.scss']
})
export class HighlightSelectorComponent {
    @Input() pageResults: PageResults;

    actionIcons = actionIcons;

    constructor() {
    }

    get highlight$(): Observable<number|undefined> {
        return this.pageResults?.highlight$;
    }

    get highlight(): number|undefined {
        return this.pageResults?.parameters$.value.highlight;
    }

    get highlightDisabled(): boolean {
        return this.pageResults?.highlightDisabled;
    }

    updateHighlightSize(instruction?: string) {
        const currentValue = this.pageResults.parameters$.value.highlight || 200;
        let newValue: number|undefined;
        if (instruction === 'on') {
            newValue = 200;
        } else if (instruction === 'more' && currentValue < 800) {
            newValue = currentValue + 200;
        } else if (instruction === 'less' && currentValue > 200) {
            newValue = currentValue - 200;
        } else if (instruction === 'off') {
            newValue = undefined;
        }
        this.pageResults.setParameters({ highlight: newValue });
    }

}
