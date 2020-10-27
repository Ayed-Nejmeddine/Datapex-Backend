import { AfterViewChecked, AfterViewInit, Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { FormBuilder, FormControl, FormGroup, Validators } from '@angular/forms';
import { first, map, startWith } from 'rxjs/operators';

import { AccountService, AlertService } from '../_services';
import { Observable } from 'rxjs';
import { parse } from 'libphonenumber-js';
import { User } from 'src/app/_models';
declare var require: any

const postalCodes = require('postal-codes-js');
@Component({
  templateUrl: 'profile.component.html',
  styleUrls: ['profile.component.scss']
})
export class ProfileComponent implements OnInit, AfterViewInit {

  form: FormGroup;
  loading = false;
  submitted = false;
  passwordRegex: RegExp = /^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*\W)/;
  countryList: { name: string, code: string, dial_code: string }[];
  phoneNumber: string = ""
  step: number = 1
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
      { type: 'validCountry', message: 'please enter a valid country (select country from the list).' }
    ],
    'postalCode': [
      { type: 'required', message: 'postalCode is required.' },
      { type: 'validPostalCode', message: 'please enter a valid postal code.' }
    ],
    'passwordactual': [
      { type: 'required', message: 'actual password is required.' },
    ],
    'password': [
      { type: 'maxlength', message: 'password length.' },
      { type: 'pattern', message: 'password must contain at least 1 lowercase alphabetical character, 1 uppercase alphabetical character, 1 numeric character, 1 special character.' },
    ],
    'passwordVerif': [
      { type: 'passwordNotMatch', message: 'password Not Match.' },
    ],
  }

  filteredCountries: Observable<any[]>;

  user: User;


  constructor(
    private formBuilder: FormBuilder,
    private route: ActivatedRoute,
    private router: Router,
    private accountService: AccountService,
    private alertService: AlertService
  ) {
    this.accountService.user.subscribe(x => {
      this.user = x
      if (!this.user)
        this.router.navigateByUrl('/users/login');
    });
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
        postalCode: new FormControl('', Validators.compose([
          Validators.required,
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
          Validators.pattern("^[0-9]+(\.[0-9][0-9]?)?$")
        ])),
        passwordactual: new FormControl('', Validators.compose([
        ])),
        password: new FormControl('', Validators.compose([
          Validators.maxLength(30),
          Validators.pattern(this.passwordRegex)
        ])),
        passwordVerif: new FormControl('', Validators.compose([
        ])),
      }, {
      validators: [this.password.bind(this), this.validCountry.bind(this), this.validPhone.bind(this), this.validPostalCode.bind(this)]
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

  ngAfterViewInit(): void {
    setTimeout(() => {
      this.form.patchValue({
        firstName: this.user.firstName,
        lastName: this.user.firstName,
        email: this.user.email,
        companyName: this.user.profile.company_name,
        postalCode: this.user.profile.postalCode ? this.user.profile.postalCode : '',
        phone: (this.user.profile.phone && this.user.profile.country) ? this.cutPhone(this.user.profile.phone, this.user.profile.country) : '',
        country: this.getCountryByCode(this.user.profile.country)
      });
    }, 100)
  }

  cutPhone(phone, countrycode) {
    let codeLength = this.getCountryByCode(countrycode, false, true).length
    let phoneParsed = phone.substring(codeLength);
    return phoneParsed
  }

  password(formGroup: FormGroup) {
    const { value: passwordActual } = formGroup.get('passwordactual');
    const { value: password } = formGroup.get('password');
    const { value: passwordVerif } = formGroup.get('passwordVerif');
    let error = (password === passwordVerif) ? null : { passwordNotMatch: true };
    let errorActual = (password === "" && passwordVerif === "") ? null : { required: true };
    let errorNew = (password !== "") ? this.passwordRegex.test(password) ? null : { pattern: true } : { pattern: true, required: true };
    formGroup.get('passwordVerif').setErrors(error);
    if (passwordActual !== "") {
      formGroup.get('password').setErrors(errorNew);
      formGroup.get('passwordactual').setErrors(null);
    } else {
      formGroup.get('passwordactual').setErrors(errorActual);
      formGroup.get('password').setErrors(null);
    }
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
        state.name.toLowerCase().indexOf(country.toLowerCase()) === 0);
      if (resultsearch.length == 1 && resultsearch[0].dial_code == code) {
        exist = true;
        if (value) {
          return resultsearch[0].code;
        }
        if (dial) {
          return resultsearch[0].dial_code;
        }
      }
    }

    return exist;
  }

  getCountryByCode(countrycode, codevalue = false, dialvalue = false) {
    if (countrycode) {
      let resultsearch: any = this.countryList.filter(state =>
        state.code.toLowerCase().indexOf(countrycode.toLowerCase()) === 0);
      if (resultsearch.length == 1 && resultsearch[0].code == countrycode) {
        if (codevalue) {
          return resultsearch[0].code;
        }
        if (dialvalue) {
          return resultsearch[0].dial_code;
        }
        return `${resultsearch[0].name}|${resultsearch[0].dial_code}`
      }
    }
    return "";
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
    let country_value = this.existCountry(countrycode, true)
    this.phoneNumber = `${dial}${this.form.value.phone}`
    let data: any = {
      firstName: this.form.value.firstName,
      lastName: this.form.value.lastName,
      username: this.form.value.email,
      email: this.form.value.email,
      passwordactual: this.form.value.password,
      password1: this.form.value.password,
      password2: this.form.value.passwordVerif,
      profile: {
        id: this.user.profile.id,
        company_name: this.form.value.companyName,
        phone: this.phoneNumber,
        country: country_value,
        postalCode: this.form.value.postalCode,
      }
    }

    this.accountService.updateAccount(data)
      .pipe(first())
      .subscribe({
        next: () => {
          this.accountService.getCurrentUser().subscribe({
            next: () => {
              this.loading = false;
              this.alertService.success('Modifcation de compte effectuée avec succés', { keepAfterRouteChange: true });
            },
            error: error => {
              this.alertService.errorlaunch(error);
              this.loading = false;
            }
          });
        },
        error: error => {
          this.alertService.errorlaunch(error);
          this.loading = false;
        }
      });
  }

}
