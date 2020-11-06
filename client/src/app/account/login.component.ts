import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { first } from 'rxjs/operators';

import { AccountService, AlertService } from '../_services';
import { User } from 'src/app/_models';
import { ExitStatus } from 'typescript';
@Component({
    templateUrl: 'login.component.html',
    styleUrls: ['login.component.scss']
})
export class LoginComponent implements OnInit {

    form: FormGroup;
    loading = false;
    submitted = false;
    typepassword = true;
    showCodeModal: boolean = false;
    user: User;
    userPhone: string = ""

    constructor(
        private formBuilder: FormBuilder,
        private route: ActivatedRoute,
        private router: Router,
        private accountService: AccountService,
        private alertService: AlertService
    ) {
        this.accountService.user.subscribe(x => this.user = x);
    }

    ngOnInit() {
        this.form = this.formBuilder.group({
            username: ['', Validators.required],
            password: ['', Validators.required]
        });

    }

    // convenience getter for easy access to form fields
    get f() { return this.form.controls; }

    onSubmit() {
        this.submitted = true;

        // reset alerts on submit
        this.alertService.clear();

        // stop here if form is invalid
        if (this.form.invalid) {
            return;
        }

        this.loading = true;
        this.accountService.login(this.f.username.value, this.f.password.value)
            .pipe(first())
            .subscribe({
                next: (data) => {
                    //if(data.profile.)
                    this.accountService.getCurrentUser().subscribe({
                        next: (data) => {
                            let aux: any = data;
                            if (!aux.profile.email_is_verified) {
                                this.alertService.error("Veuillez confirmer votre adresse email !");
                                return;
                            }
                            if (!aux.profile.phone_is_verified) {
                                this.userPhone = aux.profile.phone;
                                this.showCodeModal = true;
                                this.loading = false;
                                return;
                            }
                            // get return url from query parameters or default to home page
                            const returnUrl = '/main';
                            
                            setTimeout(() => {
                                this.router.navigate([returnUrl]);
                                this.alertService.success("Bienvenue");
                            }, 100)
                            //window.location.reload();

                        },
                        error: error => {
                            this.alertService.errorlaunch(error);
                            this.loading = false;
                        }
                    });


                },
                error: error => {
                    this.alertService.errorlaunch(error);
                    this.loading = false;
                }
            })
    }

    hideCodeModal() {
        this.showCodeModal = false
    }

    getIntroducedCode(code) {
        this.onSubmit()
    }

}
