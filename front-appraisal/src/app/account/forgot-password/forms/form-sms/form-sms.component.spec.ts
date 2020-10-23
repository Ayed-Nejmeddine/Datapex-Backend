import { ComponentFixture, TestBed } from '@angular/core/testing';

import { FormSmsComponent } from './form-sms.component';

describe('FormSmsComponent', () => {
  let component: FormSmsComponent;
  let fixture: ComponentFixture<FormSmsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ FormSmsComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(FormSmsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
