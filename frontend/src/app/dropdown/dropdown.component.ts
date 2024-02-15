import {
    Component,
    ElementRef,
    EventEmitter,
    HostListener,
    Input,
    Output,
    OnDestroy,
    HostBinding,
    AfterContentInit,
    ContentChild,
    ContentChildren,
    QueryList,
} from '@angular/core';
import { Observable, Subject, Subscription } from 'rxjs';
import { debounceTime } from 'rxjs/operators';
import * as _ from 'lodash';
import { actionIcons } from '../shared/icons';
import { DropdownMenuDirective } from './dropdown-menu.directive';
import { DropdownItemDirective } from './dropdown-item.directive';

@Component({
    selector: 'ia-dropdown',
    templateUrl: './dropdown.component.html',
    styleUrls: ['./dropdown.component.scss'],
})
export class DropdownComponent<T> implements AfterContentInit, OnDestroy  {
    @HostBinding('class') classes = 'control';
    @Input()
    public canDeselect = false;

    @Input()
    public value: T | undefined = undefined;

    @Input()
    public disabled = false;

    @Input()
    public styleClass: string;

    @Input()
    public options: T[] = [];

    @Input()
    public placeholder = '';

    @Input()
    public optionLabel: keyof T | undefined = undefined;

    @Input() icon: any;

    @ContentChild(DropdownMenuDirective) menu: DropdownMenuDirective;

    @Output()
    public onChange = new EventEmitter<T>();

    public showDropdown = false;

    actionIcons = actionIcons;

    private changeSubject = new Subject<T | undefined>();
    private changeSubscription: Subscription;

    private lodash = _;

    constructor(private elementRef: ElementRef) {
        // don't trigger a lot of events when a user is quickly looping through the options
        // for example using the keyboard arrows
        this.changeSubscription = this.changeSubject
            .pipe(debounceTime(100))
            .subscribe((value) => this.onChange.next(value));
    }

    @HostListener('document:click', ['$event'])
    onClickOut(event) {
        if (!this.elementRef.nativeElement.contains(event.target)) {
            this.showDropdown = false;
        }
    }

    ngAfterContentInit(): void {
        this.menu.selection$.subscribe(data => this.onChange.next(data));
    }

    ngOnDestroy() {
        this.changeSubscription.unsubscribe();
    }

    public toggleDropdown() {
        this.showDropdown = !this.showDropdown;
    }

}

enum KeyCode {
    Up = 38,
    Down = 40,
}
