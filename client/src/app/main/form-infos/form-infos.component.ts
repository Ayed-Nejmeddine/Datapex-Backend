import { AfterViewChecked, AfterViewInit, Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { FormBuilder, FormControl, FormGroup, Validators } from '@angular/forms';
import { first, map, startWith } from 'rxjs/operators';

import { AccountService, AlertService } from '../../_services';
import { Observable } from 'rxjs';
import { parse } from 'libphonenumber-js';
import { User } from 'src/app/_models';
@Component({
  selector: 'app-form-infos',
  templateUrl: './form-infos.component.html',
  styleUrls: ['./form-infos.component.scss']
})
export class FormInfosComponent implements OnInit, AfterViewInit {

  form: FormGroup;
  loading = false;
  submitted = false;
  showCodeModal = false;
  passwordRegex: RegExp = /^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*\W)/;
  countryList: { name: string, code: string, dial_code: string }[];
  phoneNumber: string = ""
  step: number = 1
  error_messages = {
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
  }
  user: User;
  displayForm: boolean = false;
  filteredCountries: Observable<any[]>;
  constructor(private formBuilder: FormBuilder, private accountService: AccountService, private router: Router, private alertService: AlertService) {
    this.accountService.user.subscribe(x => {
      this.user = x
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

    this.form = this.formBuilder.group(
      {
        country: new FormControl('', Validators.compose([

        ])),
        email: new FormControl('', Validators.compose([
          Validators.required,
          Validators.minLength(6),
          Validators.maxLength(50),
          Validators.pattern("^[a-z0-9._%+-]+@[a-z0-9.-]+\\.[a-z]{2,4}$")
        ])),
        phone: new FormControl('', Validators.compose([
          Validators.required,
          Validators.pattern("^[0-9]+(\.[0-9][0-9]?)?$")
        ])),

      }, {
      validators: [this.validPhone.bind(this)]
    });


  }

  filterCountries(name: string) {
    return this.countryList.filter(state =>
      state.name.toLowerCase().indexOf(name.toLowerCase()) === 0 ||  state.code.toLowerCase().indexOf(name.toLowerCase()) === 0);
  }

  onEnter(evt: any) {
  }

  validPhone(formGroup: FormGroup) {
    const { value: phone } = formGroup.get('phone');
    const { value: country } = formGroup.get('country');

    let error = this.parseWithLibphonenumber(phone, country) ? null : { validPhone: true };
    formGroup.get('phone').setErrors(error);
    return error;
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
        email: this.user.email,
        phone: (this.user.profile.phone && this.user.profile.country) ? this.cutPhone(this.user.profile.phone, this.user.profile.country) : '',
        country: this.getCountryByCode(this.user.profile.country)
      });
    }, 100)
  }

  reinitializeData() {
    this.displayForm = false
    setTimeout(() => {
      this.form.patchValue({
        email: this.user.email,
        phone: (this.user.profile.phone && this.user.profile.country) ? this.cutPhone(this.user.profile.phone, this.user.profile.country) : '',
        country: this.getCountryByCode(this.user.profile.country)
      });
    }, 500)
  }

  ngAfterViewInit(): void {
    this.reinitializeData()
  }

  cutPhone(phone, countrycode) {
    let codeLength = this.getCountryByCode(countrycode, false, true).length
    let phoneParsed = phone.substring(codeLength);
    return phoneParsed
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
        return `${resultsearch[0].code}|${resultsearch[0].dial_code}`
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
        if (dial) {
          return resultsearch[0].dial_code;
        }
      }
    }

    return exist;
  }


  // convenience getter for easy access to form fields
  get f() { return this.form.controls; }

  onSubmitVerification() {
    this.submitted = true;

    // reset alerts on submit
    this.alertService.clear();

    // stop here if form is invalid
    if (this.form.invalid) {
      return;
    }

    let countrycode = this.form.value.country;
    let dial = this.existCountry(countrycode, false, true)
    let country_value = this.existCountry(countrycode, true)
    this.phoneNumber = `${dial}${this.form.value.phone}`
    if(this.form.value.email !== this.user.email || this.phoneNumber !== this.user.profile.phone){
      this.showCodeModal = true;
      return;
    }else{
      this.displayForm = false
    }
    //this.loading = true;
    
  }

  hideCodeModal(){
    this.showCodeModal = false
  }

  getIntroducedCode(code){
    this.onSubmit()
  }


  onSubmit() {
    this.submitted = true;
    // reset alerts on submit
    this.alertService.clear();

    // stop here if form is invalid
    if (this.form.invalid) {
      return;
    }

    
    let countrycode = this.form.value.country;
    let dial = this.existCountry(countrycode, false, true)
    let country_value = this.existCountry(countrycode, true)
    this.phoneNumber = `${dial}${this.form.value.phone}`
    

    var formData = new FormData();
    formData.append('username', this.form.value.email)
    formData.append('email', this.form.value.email)
    formData.append('first_name', this.user.firstName)
    formData.append('last_name', this.user.lastName)
    formData.append('profile.id', this.user.profile.id)
    formData.append('profile.phone', this.phoneNumber)
    formData.append('profile.country', country_value)
    formData.append('profile.company_name', this.user.profile.company_name)
    formData.append('profile.city', this.user.profile.city)
    formData.append('profile.occupation', this.user.profile.occupation)
    formData.append('profile.postalCode', this.user.profile.postalCode ? this.user.profile.postalCode : null)

    this.accountService.updateAccount(formData)
      .pipe(first())
      .subscribe({
        next: () => {
          this.accountService.getCurrentUser().subscribe({
            next: () => {
              this.displayForm = false
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
