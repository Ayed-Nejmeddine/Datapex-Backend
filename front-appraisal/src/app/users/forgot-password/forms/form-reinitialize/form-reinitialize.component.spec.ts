import { ComponentFixture, TestBed } from '@angular/core/testing';

import { FormReinitializeComponent } from './form-reinitialize.component';

describe('FormReinitializeComponent', () => {
  let component: FormReinitializeComponent;
  let fixture: ComponentFixture<FormReinitializeComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ FormReinitializeComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(FormReinitializeComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
