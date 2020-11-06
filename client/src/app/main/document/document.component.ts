import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { Document, User } from '@app/_models';
import { AccountService, AlertService, DocumentService } from '@app/_services';

@Component({
  selector: 'app-document',
  templateUrl: './document.component.html',
  styleUrls: ['./document.component.scss']
})
export class DocumentComponent implements OnInit {
  document: Document;
  user: User;
  constructor(
    private activatedRoute: ActivatedRoute,
    private documentService: DocumentService,
    private alertService: AlertService,
    private accountService: AccountService,
    private router: Router
  ) {
    this.accountService.user.subscribe(x => {
      this.user = x
      if (!this.user)
        this.router.navigateByUrl('/account/login');
    });
  }

  ngOnInit(): void {
    this.activatedRoute.params.subscribe(params => {
      if (params.id) {
        this.documentService.getById(params.id).subscribe(data => {
          this.document = data;
        },
          error => {
            this.alertService.errorlaunch(error)
          });
      }

    });
  }

}
