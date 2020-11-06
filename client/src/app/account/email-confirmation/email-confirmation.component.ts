import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { AccountService, AlertService } from '@app/_services';
import { first } from 'rxjs/operators';

@Component({
  selector: 'app-email-confirmation',
  templateUrl: './email-confirmation.component.html',
  styleUrls: ['./email-confirmation.component.scss']
})
export class EmailConfirmationComponent implements OnInit {
  token: string = null;
  loading: boolean = true;
  confirmed: boolean = false;
  constructor(private route: ActivatedRoute, private accountService: AccountService, private alertService : AlertService) { }

  ngOnInit(): void {
    this.route.queryParams.subscribe(params => {
      if (params.token){
        this.token = params.token
        this.verfyAccount(this.token)
      }

    });
  }

  verfyAccount(token){
    this.accountService.verifyAccount(token)
    .pipe(first())
    .subscribe({
      next: () => {
        this.alertService.success('Compte confirmé !', { keepAfterRouteChange: true});   
        this.loading = false       
        this.confirmed = true       
      },
      error: error => {
        this.alertService.errorlaunch(error);
        this.confirmed = false       
        this.loading = false       
      }
    });
  }

}
