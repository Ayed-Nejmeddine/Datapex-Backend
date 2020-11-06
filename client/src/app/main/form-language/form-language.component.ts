import { User } from '@app/_models';
import { HttpClient, HttpEventType, HttpResponse } from '@angular/common/http';
import { Component, ElementRef, ViewChild, OnInit, AfterViewInit } from '@angular/core';
import { Router } from '@angular/router';
import { AccountService, AlertService } from 'src/app/_services';
import { FormBuilder, FormControl, FormGroup, Validators } from '@angular/forms';
import { first } from 'rxjs/operators';
@Component({
  selector: 'app-form-language',
  templateUrl: './form-language.component.html',
  styleUrls: ['./form-language.component.scss']
})
export class FormLanguageComponent implements OnInit {

  form: FormGroup;
  loading = false;
  submitted = false;
  displayedLanguage = ""
  error_messages = {
    'language': [
      { type: 'required', message: 'password is required.' },
    ],
  }
  languages = [
    {
      code: "fr",
      name: "Français"
    },
    {
      code: "en",
      name: "Anglais"
    },
  ]
  user: User;
  displayForm: boolean = false;
  constructor(private formBuilder: FormBuilder, private accountService: AccountService, private router: Router, private http: HttpClient, private alertService: AlertService) {
    this.accountService.user.subscribe(x => {
      this.user = x
    });

    this.form = this.formBuilder.group(
      {
        language: new FormControl('', Validators.compose([
          Validators.required,
        ]))
      });
  }

  ngOnInit(): void {

    this.accountService.user.subscribe(x => {
      this.user = x
      let language = this.languages.filter(x => x.code === this.user.profile.language);
      this.displayedLanguage = language.length > 0 ?  language[0].name : "";
    });

  }
  displayFormFn() {
    this.displayForm = true
    this.form.patchValue({
      language: this.user.profile.language
    })
  }

  reinitializeData() {
    this.displayForm = false
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


    var formData = new FormData();
    formData.append('username', this.user.email)
    formData.append('email', this.user.email)
    formData.append('first_name', this.user.firstName)
    formData.append('last_name', this.user.lastName)
    formData.append('profile.id', this.user.profile.id)
    formData.append('profile.phone', this.user.profile.phone)
    formData.append('profile.country',this.user.profile.country)
    formData.append('profile.company_name', this.user.profile.company_name)
    formData.append('profile.city', this.user.profile.city)
    formData.append('profile.occupation', this.user.profile.occupation)
    formData.append('profile.language', this.form.value.language)

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

  ngAfterViewInit(): void {
    this.reinitializeData()
  }

}
