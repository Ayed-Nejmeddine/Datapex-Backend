import { User } from '@app/_models';
import { HttpClient, HttpEventType, HttpResponse } from '@angular/common/http';
import { Component, ElementRef, ViewChild, OnInit, AfterViewInit } from '@angular/core';
import { Router } from '@angular/router';
import { AccountService, AlertService } from 'src/app/_services';
import { FormBuilder, FormControl, FormGroup, Validators } from '@angular/forms';
import { first } from 'rxjs/operators';
declare var require: any

const postalCodes = require('postal-codes-js');
@Component({
  selector: 'app-form-profile',
  templateUrl: './form-profile.component.html',
  styleUrls: ['./form-profile.component.scss']
})
export class FormProfileComponent implements OnInit, AfterViewInit {
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
    'occupation': [
      { type: 'required', message: 'occupation is required.' },
      { type: 'minlength', message: 'occupation length.' },
    ],
    'postalCode': [
      { type: 'required', message: 'postalCode is required.' },
      { type: 'validPostalCode', message: 'please enter a valid postal code.' }
    ],
    'city': [
      { type: 'required', message: 'city is required.' },
    ],
  }
  user: User;
  displayForm: boolean = false;

  constructor(private formBuilder: FormBuilder, private accountService: AccountService, private router: Router, private http: HttpClient, private alertService: AlertService) {
    this.accountService.user.subscribe(x => {
      this.user = x
    });

    this.accountService.getCountries()
      .subscribe(countries => {
        let data: any = countries
        this.countryList = data;
      });

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
        occupation: new FormControl('', Validators.compose([
          Validators.required,
          Validators.minLength(3),
        ])),
        postalCode: new FormControl('', Validators.compose([
          Validators.required,
          Validators.pattern("^[0-9]+(\.[0-9][0-9]?)?$")
        ])),
        city: new FormControl('', Validators.compose([
          Validators.required
        ])),

      }, {
      validators: [this.validPostalCode.bind(this)]
    });


  }

  ngOnInit(): void {
    this.accountService.user.subscribe(x => {
      this.user = x
    });


  }

  displayFormFn() {
    this.displayForm = true
    setTimeout(() => {
      this.form.patchValue({
        firstName: this.user.firstName,
        lastName: this.user.lastName,
        companyName: this.user.profile.company_name,
        occupation: this.user.profile.occupation,
        city: this.user.profile.city,
        postalCode: this.user.profile.postalCode ? this.user.profile.postalCode : '',
      });
    }, 100)
  }

  reinitializeData() {
    this.displayForm = false
    setTimeout(() => {
      this.form.patchValue({
        firstName: this.user.firstName,
        lastName: this.user.lastName,
        companyName: this.user.profile.company_name,
        occupation: this.user.profile.occupation,
        city: this.user.profile.city,
        postalCode: this.user.profile.postalCode ? this.user.profile.postalCode : '',
      });
    }, 500)
  }


  validPostalCode(formGroup: FormGroup) {
    const { value: postalCode } = formGroup.get('postalCode');
    let country = this.user.profile.country;
    let error = this.parseWithPostalCodes(postalCode, country) ? null : { validPostalCode: true };
    formGroup.get('postalCode').setErrors(error);
    return error;
  }

  parseWithPostalCodes(postalCode, countrycode) {
    let valid = false;
    if (this.countryList) {
      let existCode = this.existCountry(countrycode, true)
      if (existCode) {
        let countryCodeArray = countrycode.split('|')
        let code = countryCodeArray[1]
        let validpostalcode = postalCodes.validate(existCode.toLowerCase(), postalCode)
        if (validpostalcode === true) {
          valid = true;
        }
      }
    }

    return valid;
  }

  existCountry(countrycode, value = false, dial = false) {
    let exist = false;
    if (countrycode) {
      let resultsearch: any = this.countryList.filter(state =>
        state.code.toLowerCase().indexOf(countrycode.toLowerCase()) === 0);
      if (resultsearch.length == 1 && resultsearch[0].code == countrycode) {
        exist = true;
        if (value) {
          return resultsearch[0].code;
        }
        if (dial) {
          return resultsearch[0].dial_code;
        }
        return `${resultsearch[0].name}|${resultsearch[0].dial_code}`
      }
    }
    return exist;
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
    formData.append('username', this.user.email)
    formData.append('email', this.user.email)
    formData.append('first_name', this.form.value.firstName)
    formData.append('last_name', this.form.value.firstName)
    formData.append('profile', "profile")
    formData.append('profile.id', this.user.profile.id)
    formData.append('profile.phone', this.user.profile.phone)
    formData.append('profile.country', this.user.profile.country)
    formData.append('profile.company_name', this.form.value.companyName)
    formData.append('profile.city', this.form.value.city)
    formData.append('profile.occupation', this.form.value.occupation)
    formData.append('profile.postalCode', this.form.value.postalCode ? this.form.value.postalCode : null)


    this.accountService.updateAccount(formData)
      .pipe(first())
      .subscribe({
        next: () => {
          this.accountService.getCurrentUser().subscribe({
            next: () => {
              this.displayForm = false
              this.loading = false;
              this.alertService.success('Modifcation des informations de profil effectuée avec succés', { keepAfterRouteChange: true });
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

  ngAfterViewInit(): void {
    this.reinitializeData()
  }

}
