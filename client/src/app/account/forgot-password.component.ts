import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormControl, FormGroup, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { AccountService, AlertService } from 'src/app/_services';
import { parse } from 'libphonenumber-js';
import { first, map, startWith } from 'rxjs/operators';
import { Observable } from 'rxjs';

@Component({
  selector: 'app-forgot-password',
  templateUrl: 'forgot-password.component.html',
  styleUrls: ['forgot-password.component.scss']
})
export class ForgotPasswordComponent implements OnInit {
  step: number = 1;
  golobalTelephone: string = "";
  golobalCode: string = "";

  constructor(
    private formBuilder: FormBuilder,
    private route: ActivatedRoute,
    private router: Router,
    private accountService: AccountService,
    private alertService: AlertService
  ) { }

  ngOnInit(): void {

  }

  getIntroducedPhoneNumber(phone){
    this.golobalTelephone = phone;
    this.step = 2;
  }
  getIntroducedCode(code){
    this.golobalCode = code;
    this.step = 3;
  }

  getDoneModification(done){
    if(done){
      this.step = 4;
    }

  }
}
