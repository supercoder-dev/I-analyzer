import { ComponentFixture, TestBed, waitForAsync } from '@angular/core/testing';

import { commonTestBed } from '../common-test-bed';

import { FilterManagerComponent } from './filter-manager.component';
import { mockCorpus, mockCorpus2 } from '../../mock-data/corpus';
import { QueryModel } from '../models';

describe('FilterManagerComponent', () => {
  let component: FilterManagerComponent;
  let fixture: ComponentFixture<FilterManagerComponent>;

  beforeEach(waitForAsync(() => {
    commonTestBed().testingModule.compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(FilterManagerComponent);
    component = fixture.componentInstance;
    component.corpus = mockCorpus;
    component.queryModel = new QueryModel(mockCorpus);
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
    expect(component.potentialFilters.length).toEqual(2);
  });

  it('resets filters when corpus changes', () => {
    component.corpus = mockCorpus2;
    component.queryModel = new QueryModel(mockCorpus2);
    fixture.detectChanges();
    expect(component.potentialFilters.length).toEqual(1);
    expect(component.potentialFilters[0].adHoc).toBeTrue();

    component.corpus = mockCorpus;
    component.queryModel = new QueryModel(mockCorpus);
    fixture.detectChanges();
    expect(component.potentialFilters.length).toEqual(2);
    expect(component.potentialFilters[0].adHoc).toBeFalse();

});

  it('toggles filters on and off', async () => {
    const filter = component.potentialFilters.find(f => f.corpusField.name === 'great_field');
    expect(component.queryModel.filters.length).toBe(0);
    filter.toggle();
    expect(component.queryModel.filters.length).toBe(1);
  });
});
