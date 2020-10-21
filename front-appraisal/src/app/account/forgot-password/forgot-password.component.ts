import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-forgot-password',
  templateUrl: './forgot-password.component.html',
  styleUrls: ['./forgot-password.component.scss']
})
export class ForgotPasswordComponent implements OnInit {
  step: number = 1;
  loading = false;
  resend = false;
  email = "";
  code = "";
  password1 = "";
  password2 = "";

  constructor(private router: Router) { }

  ngOnInit(): void {
  }

  nextStep() {
    if (this.step == 4)
      this.router.navigate(['/login'])
    this.loading = true;
    switch (this.step){
      case 1:
        this.sendCode()
        break;
      case 2:
        this.verifCode()
        break;
      case 3:
        this.modifPassword()
        break;
    }
    setTimeout(() => {
      this.loading = false;
      this.step++;
    }, 1000);

  }

  sendCode(){
    setTimeout(() => {
      this.resend = false;
    }, 1000);
  }

  verifCode(){

  }

  modifPassword(){

  }

}
