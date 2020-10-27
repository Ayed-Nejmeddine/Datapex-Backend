import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { User } from 'src/app/_models';
import { AccountService } from 'src/app/_services';
@Component({ templateUrl: 'home.component.html', styleUrls : ['home.component.scss'] })
export class HomeComponent {
    toggled: boolean = false;
    togglePopupProfile: boolean = false;
    user: User;
  
    constructor(private accountService: AccountService, private router: Router) {
      this.accountService.user.subscribe(x => {
        this.user = x
        if(!this.user)
      this.router.navigateByUrl('/account/login');
      } );
    }
    ngOnInit(): void {
      
    }
    logout() {
      this.togglePopupProfile = false;
      this.accountService.logout();
    }
  
    gotoProfile() {
      this.router.navigateByUrl('/profile');
    }
}