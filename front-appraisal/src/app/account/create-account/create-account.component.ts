import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { FormBuilder, FormControl, FormGroup, Validators } from '@angular/forms';
import { first } from 'rxjs/operators';

import { AccountService, AlertService } from '../../_services';

@Component({
  selector: 'app-create-account',
  templateUrl: './create-account.component.html',
  styleUrls: ['./create-account.component.scss']
})
export class CreateAccountComponent implements OnInit {
    form: FormGroup;
    loading = false;
    submitted = false;
    passwordRegex: RegExp = /^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*\W)/;

    error_messages = {
      'firstName': [
        { type: 'required', message: 'First Name is required.' },
        { type: 'minlength', message: 'firstName length.' },
      ],
  
      'lastName': [
        { type: 'required', message: 'Last Name is required.' },
        { type: 'minlength', message: 'lastName length.' },
      ],
      'email': [
        { type: 'required', message: 'Email is required.' },
        { type: 'minlength', message: 'Email length.' },
        { type: 'maxlength', message: 'Email length.' },
        { type: 'pattern', message: 'please enter a valid email address.' },
      ],
      'phone': [
        { type: 'required', message: 'Phone is required.' },
        { type: 'minlength', message: 'Phone length.' },
        { type: 'maxlength', message: 'Phone length.' },
        { type: 'pattern', message: 'please enter a valid Phone number.' }
      ],
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

    ngOnInit() {
        this.form = this.formBuilder.group(
        {
          firstName: new FormControl('', Validators.compose([
            Validators.required,
            Validators.minLength(3),
          ])),
          lastName: new FormControl('', Validators.compose([
            Validators.required,
            Validators.minLength(3),
          ])),
          country: new FormControl('', Validators.compose([
            Validators.required
          ])),
          postalCode: new FormControl('', Validators.compose([
            Validators.required,
            Validators.minLength(5),
            Validators.pattern("^[0-9]+(\.[0-9][0-9]?)?$")
          ])),
          email: new FormControl('', Validators.compose([
            Validators.required,
            Validators.minLength(6),
            Validators.maxLength(30),
            Validators.pattern("^[a-z0-9._%+-]+@[a-z0-9.-]+\\.[a-z]{2,4}$")
          ])),
          phone: new FormControl('', Validators.compose([
            Validators.required,
            Validators.minLength(8),
            Validators.maxLength(8),
            Validators.pattern("^[0-9]+(\.[0-9][0-9]?)?$")
          ])),
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
          validators: this.password.bind(this)
        });
    }

    password(formGroup: FormGroup) {
      const { value: password } = formGroup.get('password');
      const { value: passwordVerif } = formGroup.get('passwordVerif');
      let error =  (password === passwordVerif) ? null : { passwordNotMatch: true };
      formGroup.get('passwordVerif').setErrors(error);
      return error;
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
        let data : any = {
          firstName : this.form.value.firstName,
          lastName : this.form.value.lastName,
          country : this.form.value.country,
          postalCode : this.form.value.postalCode,
          email : this.form.value.email,
          phone : this.form.value.phone,
          password1 : this.form.value.password,
          password2 : this.form.value.passwordVerif
        }
        this.accountService.register(data)
            .pipe(first())
            .subscribe({
                next: () => {
                    this.alertService.success('Registration successful', { keepAfterRouteChange: true });
                    this.router.navigate(['/login'], { relativeTo: this.route });
                },
                error: error => {
                    this.alertService.error(error);
                    this.loading = false;
                }
            });
    }
}
