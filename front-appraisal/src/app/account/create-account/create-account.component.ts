import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { FormBuilder, FormControl, FormGroup, Validators } from '@angular/forms';
import { first, map, startWith } from 'rxjs/operators';

import { AccountService, AlertService } from '../../_services';
import { Observable } from 'rxjs';
import { parse } from 'libphonenumber-js';
declare var require: any

const postalCodes = require('postal-codes-js');

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
  countryList: { name: string, code: string, dial_code: string }[];
  phoneNumber :  string = ""
  golobalCode :  string = ""
  step :  number = 1
  error_messages = {
    'firstName': [
      { type: 'required', message: 'First Name is required.' },
      { type: 'minlength', message: 'firstName length.' },
    ],
    'lastName': [
      { type: 'required', message: 'Last Name is required.' },
      { type: 'minlength', message: 'lastName length.' },
    ],
    'companyName': [
      { type: 'required', message: 'Company name is required.' },
      { type: 'minlength', message: 'Company name length.' },
    ],
    'email': [
      { type: 'required', message: 'Email is required.' },
      { type: 'minlength', message: 'Email length.' },
      { type: 'maxlength', message: 'Email length.' },
      { type: 'pattern', message: 'please enter a valid email address.' },
    ],
    'phone': [
      { type: 'required', message: 'Phone is required.' },
      { type: 'validPhone', message: 'please enter a valid Phone number.' }
    ],
    'country': [
      { type: 'required', message: 'country is required.' },
      //{ type: 'validCountry', message: 'please enter a valid country (select country from the list).' }
    ],
    'postalCode': [
      { type: 'required', message: 'postalCode is required.' },
      //{ type: 'validPostalCode', message: 'please enter a valid postal code.' }
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

  filteredCountries: Observable<any[]>;
  constructor(
    private formBuilder: FormBuilder,
    private route: ActivatedRoute,
    private router: Router,
    private accountService: AccountService,
    private alertService: AlertService
  ) {

  }


  filterCountries(name: string) {
    return this.countryList.filter(state =>
      state.name.toLowerCase().indexOf(name.toLowerCase()) === 0);
  }

  onEnter(evt: any) {
  }

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
        companyName: new FormControl('', Validators.compose([
          Validators.required,
          Validators.minLength(3),
        ])),
         country: new FormControl('', Validators.compose([
           
         ])),
        // postalCode: new FormControl('', Validators.compose([
        //   Validators.required,
        //   Validators.pattern("^[0-9]+(\.[0-9][0-9]?)?$")
        // ])),
        email: new FormControl('', Validators.compose([
          Validators.required,
          Validators.minLength(6),
          Validators.maxLength(30),
          Validators.pattern("^[a-z0-9._%+-]+@[a-z0-9.-]+\\.[a-z]{2,4}$")
        ])),
        phone: new FormControl('', Validators.compose([
          Validators.required,
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
      //validators: [this.password.bind(this), this.validCountry.bind(this), this.validPhone.bind(this), this.validPostalCode.bind(this)]
      validators: [this.password.bind(this), this.validPhone.bind(this)]
    });
    this.accountService.getCountries()
      .subscribe(countries => {
        let data: any = countries
        this.countryList = data;
        this.filteredCountries = this.form.get('country').valueChanges
          .pipe(
            startWith(''),
            map(state => state ? this.filterCountries(state) : this.countryList.slice())
          );
      });
  }

  password(formGroup: FormGroup) {
    const { value: password } = formGroup.get('password');
    const { value: passwordVerif } = formGroup.get('passwordVerif');
    let error = (password === passwordVerif) ? null : { passwordNotMatch: true };
    formGroup.get('passwordVerif').setErrors(error);
    return error;
  }

  validCountry(formGroup: FormGroup) {
    const { value: country } = formGroup.get('country');
    let error = this.existCountry(country) ? null : { validCountry: true };
    formGroup.get('country').setErrors(error);
    return error;
  }

  validPhone(formGroup: FormGroup) {
    const { value: phone } = formGroup.get('phone');
    const { value: country } = formGroup.get('country');

    let error = this.parseWithLibphonenumber(phone, country) ? null : { validPhone: true };
    formGroup.get('phone').setErrors(error);
    return error;
  }


  validPostalCode(formGroup: FormGroup) {
    const { value: postalCode } = formGroup.get('postalCode');
    const { value: country } = formGroup.get('country');

    let error = this.parseWithPostalCodes(postalCode, country) ? null : { validPostalCode: true };
    formGroup.get('postalCode').setErrors(error);
    return error;
  }

  existCountry(countrycode, value = false, dial = false) {
    let exist = false;
    let countryCodeArray = countrycode.split('|')
    let country = countryCodeArray[0]
    let code = countryCodeArray[1]
    if (code && country) {
      let resultsearch: any = this.countryList.filter(state =>
        state.code.toLowerCase().indexOf(country.toLowerCase()) === 0);
      if (resultsearch.length == 1 && resultsearch[0].dial_code == code) {
        exist = true;
        if (value) {
          return resultsearch[0].code;
        }
        if(dial){
          return resultsearch[0].dial_code;
        }
      }
    }

    return exist;
  }

  parseWithLibphonenumber(phone, countrycode) {
    let valid = false;
    let existCode = this.existCountry(countrycode, true)
    if (existCode) {
      let countryCodeArray = countrycode.split('|')
      let code = countryCodeArray[1]
      let countrygetted = parse(`${code}${phone}`);
      if (countrygetted && countrygetted.country && countrygetted.country.toLowerCase() == existCode.toLowerCase()) {
        valid = true;
      }
    }
    return valid;
  }


  parseWithPostalCodes(postalCode, countrycode) {
    let valid = false;
    let existCode = this.existCountry(countrycode, true)
    if (existCode) {
      let countryCodeArray = countrycode.split('|')
      let code = countryCodeArray[1]
      let validpostalcode = postalCodes.validate(existCode.toLowerCase(), postalCode)
      if (validpostalcode === true) {
        valid = true;
      }
    }
    return valid;
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
    let countrycode = this.form.value.country;
    let dial = this.existCountry(countrycode, false, true)
    this.phoneNumber = `${dial}${this.form.value.phone}`
    let data: any = {
      firstName: this.form.value.firstName,
      lastName: this.form.value.lastName,
      //country: this.form.value.country,
      //postalCode: this.form.value.postalCode,
      username: this.form.value.email,
      email: this.form.value.email,
      password1: this.form.value.password,
      password2: this.form.value.passwordVerif,
      profile : {
        companyName: this.form.value.companyName,
        phone: this.phoneNumber,
      }
    }

    this.accountService.register(data)
      .pipe(first())
      .subscribe({
        next: () => {
          this.loading = false;
          this.step++;
          this.alertService.success('Création de compte effectué avec succés', { keepAfterRouteChange: true});          
          this.alertService.success('Veuillez valider votre compte', { keepAfterRouteChange: true, order : 1 });          
          //this.router.navigate(['/login'], { relativeTo: this.route });
        },
        error: error => {
          this.alertService.error(error);
          this.loading = false;
        }
      });
  }

  getIntroducedCode(code){
    this.golobalCode = code;
    this.step = 3;
  } 
}