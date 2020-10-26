import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { User } from 'src/app/_models';
import { AccountService } from 'src/app/_services';

@Component({
  selector: 'app-main',
  templateUrl: './main.component.html',
  styleUrls: ['./main.component.scss']
})
export class MainComponent implements OnInit {

  toggled: boolean = false;
  togglePopupProfile: boolean = false;
  user: User;

  constructor(private accountService: AccountService, private router: Router) {
    this.accountService.user.subscribe(x => {
      this.user = x
      if(!this.user)
    this.router.navigateByUrl('/users/login');
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
