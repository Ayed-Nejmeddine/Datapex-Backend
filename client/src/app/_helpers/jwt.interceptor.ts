import { Injectable } from '@angular/core';
import { HttpRequest, HttpHandler, HttpEvent, HttpInterceptor } from '@angular/common/http';
import { Observable } from 'rxjs';

import { environment } from '../../environments/environment';
import { AccountService } from '../_services';

@Injectable()
export class TokenInterceptor implements HttpInterceptor {
    constructor(private accountService: AccountService) { }

    intercept(request: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
        // add auth header with jwt if user is logged in and request is to the api url
        const user = this.accountService.userValue;
        const isLoggedIn = user && user.token;
        const isApiUrl = request.url.startsWith(environment.apiUrl);
        const isCurrentUserQuery = request.url.endsWith("rest-auth/user/");
        const isPhoneVerif = request.url.endsWith("phone/register/");
        if (isLoggedIn && isApiUrl) {
            request = request.clone({
                setHeaders: {
                    Authorization: `Token ${user.token}`
                }
            });
        }else if(isCurrentUserQuery || isPhoneVerif){
            let keyObj : any = JSON.parse(localStorage.getItem('key'));
            request = request.clone({
                setHeaders: {
                    Authorization: `Token ${keyObj.key}`
                }
            });
        }

        return next.handle(request);
    }
}