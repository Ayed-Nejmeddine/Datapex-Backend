import { User } from '@app/_models';
import { HttpClient, HttpEventType, HttpResponse } from '@angular/common/http';
import { Component, ElementRef, ViewChild, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { environment } from '@environments/environment';
import { AccountService, AlertService } from 'src/app/_services';
@Component({
  selector: 'app-form-profile',
  templateUrl: './form-profile.component.html',
  styleUrls: ['./form-profile.component.scss']
})
export class FormProfileComponent implements OnInit {

  user: User;

  constructor(private accountService: AccountService, private router: Router, private http: HttpClient, private alertService : AlertService) {
    this.accountService.user.subscribe(x => {
      this.user = x
    });
  }

  ngOnInit(): void {
    this.accountService.user.subscribe(x => {
      this.user = x
    });
  }

}
