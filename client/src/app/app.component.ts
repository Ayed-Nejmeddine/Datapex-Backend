import { Component } from '@angular/core';

import { AccountService } from './_services';
import { User } from './_models';
import { Router } from '@angular/router';

@Component({ selector: 'app', templateUrl: 'app.component.html', styleUrls: ['app.component.scss'] })
export class AppComponent {
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
      this.router.navigateByUrl('/main/profile');
    }
}