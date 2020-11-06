import { User } from '@app/_models';
import { HttpClient, HttpEventType, HttpResponse } from '@angular/common/http';
import { Component, ElementRef, ViewChild, OnInit, AfterViewInit } from '@angular/core';
import { Router } from '@angular/router';
import { AccountService, AlertService } from 'src/app/_services';
import { FormBuilder, FormControl, FormGroup, Validators } from '@angular/forms';
import { first } from 'rxjs/operators';
@Component({
  selector: 'app-form-security',
  templateUrl: './form-security.component.html',
  styleUrls: ['./form-security.component.scss']
})
export class FormSecurityComponent implements OnInit {

  form: FormGroup;
  loading = false;
  submitted = false;
  passwordRegex: RegExp = /^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*\W)/;
  error_messages = {
    'passwordactual': [
      { type: 'required', message: 'password is required.' },
    ],
    'password': [
      { type: 'required', message: 'password is required.' },
      { type: 'minlength', message: 'password length.' },
      { type: 'maxlength', message: 'password length.' },
      { type: 'pattern', message: 'password must contain at least 1 lowercase alphabetical character, 1 uppercase alphabetical character, 1 numeric character, 1 special character.' },
    ],
    'passwordVerif': [
      { type: 'minlength', message: 'password length.' },
      { type: 'maxlength', message: 'password length.' },
      { type: 'passwordNotMatch', message: 'password Not Match.' },
    ],
  }
  user: User;
  displayForm: boolean = false;

  constructor(private formBuilder: FormBuilder, private accountService: AccountService, private router: Router, private http: HttpClient, private alertService: AlertService) {
    this.accountService.user.subscribe(x => {
      this.user = x
    });

    this.form = this.formBuilder.group(
      {
        passwordactual: new FormControl('', Validators.compose([
          Validators.required,
        ])),
        password: new FormControl('', Validators.compose([
          Validators.required,
          Validators.minLength(8),
          Validators.maxLength(50),
          Validators.pattern(this.passwordRegex)
        ])),
        passwordVerif: new FormControl('', Validators.compose([
          Validators.required
        ])),

      }, {
      validators: [this.password.bind(this)]
    });


  }

  ngOnInit(): void {
    this.accountService.user.subscribe(x => {
      this.user = x
    });


  }

  password(formGroup: FormGroup) {
    const { value: password } = formGroup.get('password');
    const { value: passwordVerif } = formGroup.get('passwordVerif');
    let error = (password === passwordVerif) ? null : { passwordNotMatch: true };
    formGroup.get('passwordVerif').setErrors(error);
    return error;
  }

  displayFormFn() {
    this.displayForm = true
  }

  reinitializeData() {
    this.displayForm = false
    this.submitted = false
    this.form.patchValue({
      passwordactual : '',
      password : '',
      passwordVerif : '',
    })
  }

  // convenience getter for easy access to form fields
  get f() { return this.form.controls; }


  onSubmit() {
    this.submitted = true;

    // reset alerts on submit
    this.alertService.clear();

    // stop here if form is invalid
    if (this.form.invalid) {
      return;
    }

    this.loading = true;

    var formData = new FormData();
    formData.append('old_password', this.form.value.passwordactual)
    formData.append('new_password1', this.form.value.password)
    formData.append('new_password2', this.form.value.passwordVerif)
    this.accountService.updatePassword(formData)
      .pipe(first())
      .subscribe({
        next: () => {
          this.alertService.success('Modifcation de mot de passe effectuée avec succés', { keepAfterRouteChange: true });
          this.loading = false;
          this.reinitializeData()
        },
        error: error => {
          this.alertService.errorlaunch(error);
          this.loading = false;
        }
      });
  }

  ngAfterViewInit(): void {
    this.reinitializeData()
  }


}
