import { Component } from '@angular/core';

import { AccountService } from './_services';
import { User } from './_models';
import { Router } from '@angular/router';
import { TranslateService } from '@ngx-translate/core';

@Component({ selector: 'app', templateUrl: 'app.component.html', styleUrls: ['app.component.scss'] })
export class AppComponent {
  toggled: boolean = false;
  togglePopupProfile: boolean = false;
  user: User;


  // the default locale
  locale = "fr";
  constructor(private accountService: AccountService, private router: Router, public translate: TranslateService) {
    this.accountService.user.subscribe(x => {
      this.user = x
      if (this.user)
        this.updateLocale(this.user.profile.language);
      else
        this.updateByDetectedLanguage()
    });
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

  // change locale/language at runtime
  updateLocale(locale) {
    this.locale = locale;
    const lang = locale.substring(0, 2);
    this.translate.setDefaultLang(lang);
    this.translate.get('menu.home').subscribe((res: string) => {
      console.log(res);
    });
  }

  updateByDetectedLanguage(){
    const wn : any = window.navigator;
    let lang = wn.languages ? wn.languages[0] : "fr";
    lang = lang || wn.language || wn.browserLanguage || wn.userLanguage;
    this.updateLocale(lang)
  }
}