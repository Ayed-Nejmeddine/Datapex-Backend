import { Component, ElementRef, OnInit, ViewChild } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { FormBuilder } from '@angular/forms';

import { AccountService, AlertService } from '../_services';

import { User } from 'src/app/_models';
import { environment } from '@environments/environment';
import { HttpClient, HttpEventType, HttpResponse } from '@angular/common/http';
import { first } from 'rxjs/operators';

@Component({
  templateUrl: 'profile.component.html',
  styleUrls: ['profile.component.scss']
})
export class ProfileComponent implements OnInit {

  user: User;
  @ViewChild('myInput') myInputVariable: ElementRef;
  uploadSuccess: boolean = false
  choosedImage: boolean = false
  choosedImageData: string = ""
  filesData: File[] = []
  constructor(
    private router: Router,
    private accountService: AccountService,
    private alertService: AlertService,
    private http : HttpClient
  ) {
    this.accountService.user.subscribe(x => {
      this.user = x
    });
  }

  ngOnInit() {
    this.accountService.user.subscribe(x => {
      this.user = x
    });
  }


  upload(files: File[]) {
    let sizeError = false;
    this.filesData = []
    this.choosedImage = false
    this.choosedImageData = ""
    this.uploadSuccess = false
    Array.from(files).forEach(f => {
      if (f.size > 5242880)
        sizeError = true;
    })
    if (sizeError) {
      this.alertService.error('Taille Maximum 5 MO !')
      return;
    }
    this.filesData = files
    this.choosedImage = true
    const _this: any = this
    // FileReader support
    if (FileReader && files && files.length) {
      var fr = new FileReader();
      fr.onload = function () {
        _this.choosedImageData = fr.result;
      }
      fr.readAsDataURL(files[0]);
    }
  }

  reinitializeInput() {
    this.choosedImageData = ""
    this.uploadSuccess = false
    this.choosedImage = false
    this.filesData = []
    setTimeout(() => { this.myInputVariable.nativeElement.value = ""; }, 100)
    this.alertService.clear()
  }

  saveImage() {
    this.uploadAndProgress(this.filesData)
  }

  uploadAndProgress(files: File[]) {
    var formData = new FormData();
    var profileFormData = new FormData();
    let photo: any = null
    Array.from(files).forEach(f =>{
      formData.append('photo', f)
      photo = f
    } )
    // formData.append('username', this.user.email)
    // formData.append('email', this.user.email)
    // formData.append('first_name', this.user.firstName)
    // formData.append('last_name', this.user.lastName)
    // formData.append('profile', "profile")
    // formData.append('profile[id]', this.user.profile.id)
    // formData.append('profile[phone]', this.user.profile.phone)
    // formData.append('profile[country]', this.user.profile.country)
    // formData.append('profile[company_name]', this.user.profile.company_name)
    // formData.append('profile[city]', this.user.profile.city)
    // formData.append('profile[function]', this.user.profile.function)
    // formData.append('profile[postalCode]', this.user.profile.postalCode)
    // formData.append('profile[photo]', this.user.profile.photo)
    let data: any = {
      username: this.user.email,
      email: this.user.email,
      first_name: this.user.firstName,
      last_name: this.user.lastName,
      profile: {
        id: this.user.profile.id,
        phone: this.user.profile.phone,
        country: this.user.profile.country,
        company_name: this.user.profile.company_name,
        city: this.user.profile.city,
        function: this.user.profile.function,
        postalCode: this.user.profile.postalCode,
        photo : formData
      }
    }
    this.accountService.updateAccount(data)
    .pipe(first())
    .subscribe({
      next: () => {
        this.accountService.getCurrentUser().subscribe({
          next: () => {
            this.uploadSuccess = true
            this.filesData = []
            this.alertService.success("Photo de profil mise à jours avec succés!")
            this.choosedImage = false
            this.choosedImageData = ""
            setTimeout(() => { this.myInputVariable.nativeElement.value = ""; }, 100)          },
          error: error => {
            this.alertService.errorlaunch(error);
          }
        });
      },
      error: error => {
        this.alertService.errorlaunch(error);
      }
    });
    

  }

  // password(formGroup: FormGroup) {
  //   const { value: passwordActual } = formGroup.get('passwordactual');
  //   const { value: password } = formGroup.get('password');
  //   const { value: passwordVerif } = formGroup.get('passwordVerif');
  //   let error = (password === passwordVerif) ? null : { passwordNotMatch: true };
  //   let errorActual = (password === "" && passwordVerif === "") ? null : { required: true };
  //   let errorNew = (password !== "") ? this.passwordRegex.test(password) ? null : { pattern: true } : { pattern: true, required: true };
  //   formGroup.get('passwordVerif').setErrors(error);
  //   if (passwordActual !== "") {
  //     formGroup.get('password').setErrors(errorNew);
  //     formGroup.get('passwordactual').setErrors(null);
  //   } else {
  //     formGroup.get('passwordactual').setErrors(errorActual);
  //     formGroup.get('password').setErrors(null);
  //   }
  //   return error;
  // }

}
