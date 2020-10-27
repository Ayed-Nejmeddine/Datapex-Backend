import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { FormBuilder, FormControl, FormGroup, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { AccountService, AlertService } from 'src/app/_services';
import { parse } from 'libphonenumber-js';
import { first, map, startWith } from 'rxjs/operators';
import { Observable } from 'rxjs';

@Component({
  selector: 'app-form-reinitialize',
  templateUrl: './form-reinitialize.component.html',
  styleUrls: ['./form-reinitialize.component.scss']
})
export class FormReinitializeComponent implements OnInit {
  step: number = 1;
  loading = false;
  formReinitialize: FormGroup;
  submitted = false;
  passwordRegex: RegExp = /^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*\W)/;
  @Input() phoneNumberIntroduced: string;
  @Output() doneEmitter: EventEmitter<any> = new EventEmitter();

  error_messages = {
    'password': [
      { type: 'required', message: 'password is required.' },
      { type: 'minlength', message: 'password length.' },
      { type: 'maxlength', message: 'password length.' },
      { type: 'pattern', message: 'password must contain at least 1 lowercase alphabetical character, 1 uppercase alphabetical character, 1 numeric character, 1 special character.' },
    ],
    'passwordVerif': [
      { type: 'required', message: 'password is required.' },
      { type: 'minlength', message: 'password length.' },
      { type: 'maxlength', message: 'password length.' },
      { type: 'passwordNotMatch', message: 'password Not Match.' },
    ],
  }
  constructor(
    private formBuilder: FormBuilder,
    private route: ActivatedRoute,
    private router: Router,
    private accountService: AccountService,
    private alertService: AlertService
  ) { }

  ngOnInit(): void {
    
    this.formReinitialize = this.formBuilder.group(
      {
        password: new FormControl('', Validators.compose([
          Validators.required,
          Validators.minLength(8),
          Validators.maxLength(30),
          Validators.pattern(this.passwordRegex)
        ])),
        passwordVerif: new FormControl('', Validators.compose([
          Validators.required
        ])),
      }, {
      validators: [this.password.bind(this)]
    });
  }

    // convenience getter for easy access to formReinitialize fields
    get frein() { return this.formReinitialize.controls; }

    password(formGroup: FormGroup) {
      const { value: password } = formGroup.get('password');
      const { value: passwordVerif } = formGroup.get('passwordVerif');
      let error = (password === passwordVerif) ? null : { passwordNotMatch: true };
      formGroup.get('passwordVerif').setErrors(error);
      return error;
    }

    nextStep() {
      this.submitted = true;

      // reset alerts on submit
      this.alertService.clear();
  
      // stop here if form is invalid
      if (this.formReinitialize.invalid) {
        return;
      }
      this.loading = true;
      setTimeout(() => {
        this.loading = false;
        this.emitDone()
      }, 1000);
  
    }

    emitDone(){
      this.doneEmitter.emit(true)
    }

}
