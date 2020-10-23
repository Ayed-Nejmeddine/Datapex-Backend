import { Component, EventEmitter, OnInit, Output } from '@angular/core';
import { FormBuilder, FormControl, FormGroup, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { AccountService, AlertService } from 'src/app/_services';
import { parse } from 'libphonenumber-js';
import { first, map, startWith } from 'rxjs/operators';
import { Observable } from 'rxjs';
@Component({
  selector: 'app-form-sms',
  templateUrl: './form-sms.component.html',
  styleUrls: ['./form-sms.component.scss']
})
export class FormSmsComponent implements OnInit {
  step: number = 1;
  loading = false;
  resend = false;
  formSms: FormGroup;
  submitted = false;
  countryList: { name: string, code: string, dial_code: string }[];
  filteredCountries: Observable<any[]>;
  @Output() phoneNumberEmitter: EventEmitter<any> = new EventEmitter();
  error_messages = {
    'phone': [
      { type: 'required', message: 'phone is required.' },
      { type: 'validPhone', message: 'please enter a valid Phone number.' }
    ],
    'country': [
      { type: 'required', message: 'country is required.' },
    ]
  }
  constructor(
    private formBuilder: FormBuilder,
    private route: ActivatedRoute,
    private router: Router,
    private accountService: AccountService,
    private alertService: AlertService
  ) { }

  ngOnInit(): void {
    this.formSms = this.formBuilder.group(
      {
        country: new FormControl('', Validators.compose([
        ])),
        phone: new FormControl('', Validators.compose([
          Validators.required,
          Validators.pattern("^[0-9]+(\.[0-9][0-9]?)?$")
        ])),
      }, {
      //validators: [this.password.bind(this), this.validCountry.bind(this), this.validPhone.bind(this), this.validPostalCode.bind(this)]
      validators: [this.validPhone.bind(this)]
    });

    this.accountService.getCountries()
      .subscribe(countries => {
        let data: any = countries
        this.countryList = data;
        this.filteredCountries = this.formSms.get('country').valueChanges
          .pipe(
            startWith(''),
            map(state => state ? this.filterCountries(state) : this.countryList.slice())
          );
      });
  }

    // convenience getter for easy access to formSms fields
    get fsms() { return this.formSms.controls; }


    filterCountries(name: string) {
      return this.countryList.filter(state =>
        state.name.toLowerCase().indexOf(name.toLowerCase()) === 0);
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

    nextStep() {
    this.submitted = true;

    // reset alerts on submit
    this.alertService.clear();

    // stop here if form is invalid
    if (this.formSms.invalid) {
      return;
    }

      this.loading = true;
      setTimeout(() => {
        this.loading = false;
        this.emitPhoneNumber()
      }, 1000);
  
    }

    emitPhoneNumber(){
      let countrycode = this.formSms.value.country;
      let dial = this.existCountry(countrycode, false, true)
      this.phoneNumberEmitter.emit(`${dial}${this.formSms.value.phone}`)
    }
  

}
