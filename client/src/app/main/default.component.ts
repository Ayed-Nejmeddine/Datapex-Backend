import { HttpClient, HttpEventType, HttpResponse } from '@angular/common/http';
import { Component, ElementRef, ViewChild } from '@angular/core';
import { Router } from '@angular/router';
import { environment } from '@environments/environment';
import { User } from 'src/app/_models';
import { AccountService, AlertService } from 'src/app/_services';
@Component({ templateUrl: 'default.component.html', styleUrls: ['default.component.scss'] })
export class DefaultComponent {
  toggled: boolean = false;
  togglePopupProfile: boolean = false;
  uploading: boolean = false;
  loadingerror: boolean = false;
  user: User;
  percentDone: number = 0;
  uploadSuccess: boolean;
  @ViewChild('myInput') myInputVariable: ElementRef;
  constructor(private accountService: AccountService, private router: Router, private http: HttpClient, private alertService : AlertService) {
    this.accountService.user.subscribe(x => {
      this.user = x
      if (!this.user)
        this.router.navigateByUrl('/account/login');
    });
  }
  ngOnInit(): void {
    console.log('dash')
    
  }
  logout() {
    this.togglePopupProfile = false;
    this.accountService.logout();
  }

  gotoProfile() {
    this.router.navigateByUrl('/profile');
  }


  upload(files: File[]) {
    this.loadingerror = false
    let sizeError = false;
    
    Array.from(files).forEach(f => {
      if(f.size > 524288000 )
        sizeError = true;
    })
    if(sizeError){
      this.alertService.error('Taille Maximum 500 MO !')
      this.reinitializeInput()
      return;
    }
    this.uploadAndProgress(files);
  }

  reinitializeInput(){
    this.uploading = false
    this.uploadSuccess = false
    this.loadingerror = false
    setTimeout(() => {this.myInputVariable.nativeElement.value = "";}, 100)
    this.alertService.clear()
  }

  uploadAndProgress(files: File[]) {
    var formData = new FormData();
    Array.from(files).forEach(f => formData.append('document_path', f))
    this.uploading = true;
    this.http.post(`${environment.apiUrl}/api/v1/upload-document/`, formData, { reportProgress: true, observe: 'events' })
      .subscribe(event => {
        if (event.type === HttpEventType.UploadProgress) {
          this.percentDone = Math.round(100 * event.loaded / event.total);
        } else if (event instanceof HttpResponse) {
          console.log(event)
          this.uploadSuccess = true;
          this.uploading = false;
        }
      },
      error => {
        this.loadingerror = true
        this.alertService.errorlaunch(error)
      });
  }

  analyseFile(){
    if(this.uploadSuccess){
      alert('analyse ........')
    }
  }
}