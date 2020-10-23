import { Component } from '@angular/core';
import { User } from './_models';
import { AccountService } from './_services';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  title = 'datapex';
  toggled : boolean = false;
  togglePopupProfile : boolean = false;
  user: User;

    constructor(private accountService: AccountService) {
        this.accountService.user.subscribe(x => this.user = x);
    }

    logout() {
      this.togglePopupProfile = false;
        this.accountService.logout();
    }
}
