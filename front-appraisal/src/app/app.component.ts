import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { User } from './_models';
import { AccountService } from './_services';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit {
  title = 'datapex';
  toggled: boolean = false;
  togglePopupProfile: boolean = false;
  user: User;

  constructor(private accountService: AccountService, private router: Router) {
    this.accountService.user.subscribe(x => this.user = x);
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
