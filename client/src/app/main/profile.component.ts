import { Component, ElementRef, OnInit, ViewChild } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { FormBuilder } from '@angular/forms';

import { AccountService, AlertService } from '../_services';

import { User } from 'src/app/_models';
import { environment } from '@environments/environment';
import { HttpClient, HttpEventType, HttpResponse } from '@angular/common/http';
import { first } from 'rxjs/operators';
import { ImageCroppedEvent, ImageTransform } from 'ngx-image-cropper';
import { DatePipe } from '@angular/common';

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
  fileForFormdata: File = null

  // COUNT COMPLETION 
  fieldsNumber: number = 12
  completedFields: number = 0
  notCountedField: any = ['id', 'token', 'phone_is_verified', 'email_is_verified']

  // CROP ATTRIBUTES
  showCropper = false;
  public progress: number;
  public filename: any;
  //canAccess: boolean = true;
  transform: ImageTransform = {};
  scale = 1;
  imageChangedEvent: any = '';
  cropper = {
    x1: 100,
    y1: 100,
    x2: 200,
    y2: 200
  }
  constructor(
    private router: Router,
    private accountService: AccountService,
    private alertService: AlertService,
    private http: HttpClient,
    private datePipe: DatePipe
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

  get percentCompletion(){
    this.completedFields = 0;
    this.countCompletion(this.user)
    return Math.round((this.completedFields/this.fieldsNumber)*100);
  }

  countCompletion(data) {
    if (typeof data === "object") {
        for (const property in data) {
            if(typeof data[property] === "object" ){
                this.countCompletion(data[property])
            }else{
              if(data[property] && this.notCountedField.indexOf(property) < 0)
                this.completedFields++;
            }
        }
    }
}


  upload(evt) {
    var files: File[] = evt.target.files;
    let sizeError = false;
    this.fileForFormdata = null
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
    this.choosedImage = true

    this.imageChangedEvent = evt;

  }

  reinitializeInput() {
    this.choosedImageData = ""
    this.uploadSuccess = false
    this.choosedImage = false
    this.fileForFormdata = null
    this.showCropper = false;
    setTimeout(() => { this.myInputVariable.nativeElement.value = ""; }, 100)
    this.alertService.clear()
  }

  saveImage() {
    this.uploadAndProgress()
  }

  uploadAndProgress() {
    var formData = new FormData();
    var profileFormData = new FormData();
    let photo: any = this.fileForFormdata

    formData.append('username', this.user.email)
    formData.append('email', this.user.email)
    formData.append('first_name', this.user.firstName)
    formData.append('last_name', this.user.lastName)
    formData.append('profile.id', this.user.profile.id)
    formData.append('profile.phone', this.user.profile.phone)
    formData.append('profile.country', this.user.profile.country)
    formData.append('profile.company_name', this.user.profile.company_name)
    formData.append('profile.city', this.user.profile.city)
    formData.append('profile.occupation', this.user.profile.occupation)
    formData.append('profile.photo', photo)
    this.accountService.updateAccount(formData)
      .pipe(first())
      .subscribe({
        next: () => {
          this.accountService.getCurrentUser().subscribe({
            next: () => {
              this.uploadSuccess = true
              this.fileForFormdata = null
              this.alertService.success("Photo de profil mise à jours avec succés!")
              this.choosedImage = false
              this.choosedImageData = ""
              this.showCropper = false;

              setTimeout(() => { this.myInputVariable.nativeElement.value = ""; }, 100)
            },
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


  // CROP FUNCTION

  imageCropped(event: ImageCroppedEvent) {
    setTimeout(() => {
      this.choosedImageData = event.base64
      let d = new Date()
      let extension = this.imageChangedEvent.target.files[0].name.split('.').pop();
      this.filename = `img_${this.datePipe.transform(d, "yMMdhhmmss")}${Math.floor(Math.random() * Math.floor(1000000))}.${extension}`
      var image = this.choosedImageData.substr(22);
      const imageBlob = this.dataURItoBlob(image);
      const file = new File([imageBlob], this.filename);
      this.fileForFormdata = file;
    }, 200)

  }


  dataURItoBlob(dataURI) {
    const byteString = window.atob(dataURI);
    const arrayBuffer = new ArrayBuffer(byteString.length);
    const int8Array = new Uint8Array(arrayBuffer);
    for (let i = 0; i < byteString.length; i++) {
      int8Array[i] = byteString.charCodeAt(i);
    }
    const blob = new Blob([int8Array], { type: 'image/jpeg' });
    return blob;
  }


  cropperReady() {

    // cropper ready
  }
  loadImageFailed() {
    // show message
  }

  zoomIn() {
    this.scale -= .1;
    this.transform = {
      ...this.transform,
      scale: this.scale
    };
  }

  zoomOut() {
    this.scale += .1;
    this.transform = {
      ...this.transform,
      scale: this.scale
    };
  }


  imageLoaded() {
    this.showCropper = true;
    setTimeout(() => {
      this.cropper = {
        x1: 100,
        y1: 100,
        x2: 300,
        y2: 200
      }
    });
  }
}
