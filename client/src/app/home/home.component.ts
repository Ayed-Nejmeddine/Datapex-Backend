import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router, RouterStateSnapshot } from '@angular/router';
import { User } from 'src/app/_models';
import { AccountService } from 'src/app/_services';
@Component({ templateUrl: 'home.component.html', styleUrls: ['home.component.scss'] })
export class HomeComponent implements OnInit{
  toggled: boolean = false;
  togglePopupProfile: boolean = false;
  user: User;

  constructor(private accountService: AccountService, private router: Router, private route : ActivatedRoute) {
    this.accountService.user.subscribe(x => {
      this.user = x
      if (!this.user)
        this.router.navigateByUrl('/account/login');
      else{
        this.router.navigateByUrl('/main');

       }
    });
  }
  ngOnInit(): void {
    this.accountService.user.subscribe(x => {
      this.user = x
      if (!this.user)
        this.router.navigateByUrl('/account/login');
    });
  }
  logout() {
    this.togglePopupProfile = false;
    this.accountService.logout();
  }

  gotoProfile() {
    this.router.navigateByUrl('/profile');
  }
}