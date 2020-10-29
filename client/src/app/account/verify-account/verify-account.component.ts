import { AfterViewInit, Component, EventEmitter, Input, OnInit, Output, Renderer2 } from '@angular/core';
import { FormBuilder, FormControl, FormGroup, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { AccountService, AlertService } from 'src/app/_services';
import { parse } from 'libphonenumber-js';
import { first, map, startWith } from 'rxjs/operators';
import { Observable } from 'rxjs';

@Component({
  selector: 'app-verify-account',
  templateUrl: 'verify-account.component.html',
  styleUrls: ['verify-account.component.scss']
})
export class VerifyAccountComponent implements OnInit, AfterViewInit {

  step: number = 1;
  loading = false;
  resend = false;
  formCode: FormGroup;
  fullCode: string = "";
  sessionToken: string = "";
  submitted = false;
  coderegexp: RegExp = /^[a-zA-Z0-9]*$/;
  @Input() phoneNumberIntroduced: string;
  @Output() codeEmitter: EventEmitter<any> = new EventEmitter();

  constructor(
    private formBuilder: FormBuilder,
    private route: ActivatedRoute,
    private router: Router,
    private accountService: AccountService,
    private alertService: AlertService,
    private renderer: Renderer2
  ) { }

  ngOnInit(): void {
    this.formCode = this.formBuilder.group(
      {
        code1: new FormControl('', Validators.compose([
          Validators.required,
          Validators.pattern(this.coderegexp)
        ])),
        code2: new FormControl('', Validators.compose([
          Validators.required,
          Validators.pattern(this.coderegexp)
        ])),
        code3: new FormControl('', Validators.compose([
          Validators.required,
          Validators.pattern(this.coderegexp)
        ])),
        code4: new FormControl('', Validators.compose([
          Validators.required,
          Validators.pattern(this.coderegexp)
        ])),
        code5: new FormControl('', Validators.compose([
          Validators.required,
          Validators.pattern(this.coderegexp)
        ])),
        code6: new FormControl('', Validators.compose([
          Validators.required,
          Validators.pattern(this.coderegexp)
        ])),
      });
    this.sendCode()
  }

  // convenience getter for easy access to formSms fields
  get fcode() { return this.formCode.controls; }

  nextStep() {
    this.submitted = true;

    // reset alerts on submit
    this.alertService.clear();

    // stop here if form is invalid
    if (this.formCode.invalid) {
      return;
    }
    this.loading = true;
    let code1 = this.formCode.value.code1;
    let code2 = this.formCode.value.code2;
    let code3 = this.formCode.value.code3;
    let code4 = this.formCode.value.code4;
    let code5 = this.formCode.value.code5;
    let code6 = this.formCode.value.code6;
    this.fullCode = `${code1}${code2}${code3}${code4}${code5}${code6}`;
    this.applyAccountVerification()

  }
  sendCode() {
    let phoneObject: any = {
      phone_number: this.phoneNumberIntroduced
    }
    this.accountService.sendSmsCodePhone(phoneObject)
      .pipe(first())
      .subscribe({
        next: (data) => {
          let auxData: any = data
          this.sessionToken = auxData.session_token
          this.resend = false
        },
        error: error => {
          this.alertService.errorlaunch(error);
          this.resend = false
        }
      });
  }

  applyAccountVerification() {
    let phoneEndpointObject: any = {
      phone_number: this.phoneNumberIntroduced,
      session_token: this.sessionToken,
      security_code: this.fullCode,
    }
    this.accountService.applyAccountVerificationApi(phoneEndpointObject)
      .pipe(first())
      .subscribe({
        next: (data) => {
            this.loading = false;
            this.emitPhoneNumber()
        },
        error: error => {
          this.alertService.errorlaunch(error);
          this.loading = false;
        }
      });
  }

  emitPhoneNumber() {
    this.codeEmitter.emit(`${this.fullCode}`)
  }

  ngAfterViewInit() {
    setTimeout(() => {
      var elem = this.renderer.selectRootElement(`#code_1`);
      elem.focus();
    }, 100);
  }
  keyDownCode(event) {
    if (event.key.trim() === "") {
      event.stopPropagation()
      event.preventDefault()
    }
  }
  dropCode(event) {
    let pastedText = event.dataTransfer.getData("text")
    if (pastedText.trim().replace(/\s/g, '') !== "") {
      let arraypastedText = pastedText.trim().replace(/\s/g, '').split('')
      this.formCode.patchValue({
        code1: arraypastedText[0] ? arraypastedText[0] : '',
        code2: arraypastedText[1] ? arraypastedText[1] : '',
        code3: arraypastedText[2] ? arraypastedText[2] : '',
        code4: arraypastedText[3] ? arraypastedText[3] : '',
        code5: arraypastedText[4] ? arraypastedText[4] : '',
        code6: arraypastedText[5] ? arraypastedText[5] : '',
      })
    }

  }
  fillInputCode(index, value) {
    if (value !== "") {
      if (index !== 6) {

        let focusElem: number = index + 1
        console.log(index, focusElem)
        this.focusCode(focusElem)
      }
    } else {
      if (index !== 1) {
        let focusElem: number = index - 1
        this.focusCode(focusElem)
      }
    }
  }

  focusCode(index) {
    this.renderer.selectRootElement(`#code_${index}`).focus();
  }
  onPasteCode(event) {
    let clipboardData = event.clipboardData;
    let pastedText = clipboardData.getData('text');
    let arraypastedText = pastedText.trim().replace(/\s/g, '').split('')
    this.formCode.patchValue({
      code1: arraypastedText[0] ? arraypastedText[0] : '',
      code2: arraypastedText[1] ? arraypastedText[1] : '',
      code3: arraypastedText[2] ? arraypastedText[2] : '',
      code4: arraypastedText[3] ? arraypastedText[3] : '',
      code5: arraypastedText[4] ? arraypastedText[4] : '',
      code6: arraypastedText[5] ? arraypastedText[5] : '',
    })
  }

}
