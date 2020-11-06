import { HttpClient, HttpEventType, HttpResponse } from '@angular/common/http';
import { Component, ElementRef, ViewChild } from '@angular/core';
import { Router } from '@angular/router';
import { environment } from '@environments/environment';
import { User, Document } from 'src/app/_models';
import { AccountService, AlertService, DocumentService } from 'src/app/_services';
import { saveAs } from 'file-saver';

@Component({ templateUrl: 'default.component.html', styleUrls: ['default.component.scss'] })
export class DefaultComponent {
  toggled: boolean = false;
  togglePopupProfile: boolean = false;
  uploading: boolean = false;
  loadingerror: boolean = false;
  user: User;
  percentDone: number = 0;
  uploadSuccess: boolean;
  document: Document;
  lastTreatedDocument: Document;
  @ViewChild('myInput') myInputVariable: ElementRef;
  constructor(private accountService: AccountService, private documentService: DocumentService, private router: Router, private http: HttpClient, private alertService: AlertService) {
    this.accountService.user.subscribe(x => {
      this.user = x
      if (!this.user)
        this.router.navigateByUrl('/account/login');
    });
  }
  ngOnInit(): void {
    if (this.user)
      this.documentService.lastTreatedDocument().subscribe(data => {
        this.lastTreatedDocument = data;
      },
        error => {
          this.alertService.errorlaunch(error)
        });
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
      if (f.size > 524288000)
        sizeError = true;
    })
    if (sizeError) {
      this.alertService.error('Taille Maximum 500 MO !')
      this.reinitializeInput()
      return;
    }
    this.uploadAndProgress(files);
  }

  reinitializeInput() {
    this.uploading = false
    this.uploadSuccess = false
    this.loadingerror = false
    setTimeout(() => { this.myInputVariable.nativeElement.value = ""; }, 100)
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
          this.uploadSuccess = true;
          this.uploading = false;
          let doc: any = event.body
          this.document = doc
        }
      },
        error => {
          this.loadingerror = true
          this.alertService.errorlaunch(error)
        });
  }

  analyseFile() {
    let order = 0
    if (this.uploadSuccess) {
      this.documentService.getById(this.document.id).subscribe(data => {
        this.alertService.success(`Demande d\'analyse de document ...`, { order: order })

        this.documentService.launchSyntacticAnalyse(this.document).subscribe(data => {
          this.router.navigate([`/main/document/${this.document.id}`])
          order++;
          this.alertService.success('L\'analyse Syntaxique a été lancé !', { order: order })
        },
          error => {
            this.alertService.errorlaunch(error)
          });
      },
        error => {
          this.alertService.errorlaunch(error)
        });
    }
  }

  launchSemanticAnalysis() {
    this.documentService.launchSemanticAnalyse(this.document).subscribe((data: any) => {
      this.alertService.success('L\'analyse Sémantique a été lancé !', { order: 0 })
      const blob = new Blob([data], { type: 'application/octet-stream' });
      const fileName = 'Your File Name.csv';
      saveAs(blob, fileName);
    },
      error => {
        this.alertService.errorlaunch(error)
      })
  }

  getSyntacticAnalysisResults() {
    this.documentService.getSyntacticAnalysisResults(this.document).subscribe((data: any) => {
      const blob = new Blob([data], { type: 'application/octet-stream' });
      const fileName = 'Your File Name.csv';
      saveAs(blob, fileName);
    },
      error => {
        this.alertService.errorlaunch(error)
      })
  }

  getLinksBetweenColumns() {
    this.documentService.getLinksBetweenColumns(this.document).subscribe(data => {
      alert(JSON.stringify(data))
    },
      error => {
        this.alertService.errorlaunch(error)
      });
  }
}