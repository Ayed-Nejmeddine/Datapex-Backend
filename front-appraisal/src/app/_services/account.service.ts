import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable, forkJoin } from 'rxjs';
import { map } from 'rxjs/operators';

import { environment } from '../../environments/environment';
import { User } from '../_models';

@Injectable({ providedIn: 'root' })
export class AccountService {
    private userSubject: BehaviorSubject<User>;
    public user: Observable<User>;

    constructor(
        private router: Router,
        private http: HttpClient
    ) {
        this.userSubject = new BehaviorSubject<User>(JSON.parse(localStorage.getItem('user')));
        this.user = this.userSubject.asObservable();
    }

    public get userValue(): User {
        return this.userSubject.value;
    }

    login(username, password) {
        return this.http.post<User>(`${environment.apiUrl}/rest-auth/login/`, { username, password }).pipe(map(key => {
            // store user details and jwt token in local storage to keep user logged in between page refreshes
            localStorage.setItem('key', JSON.stringify(key));
            return key;
        }));
    }

    getCurrentUser(){
        return this.http.get(`${environment.apiUrl}/rest-auth/user/`).pipe(map(user => {
            // store user details and jwt token in local storage to keep user logged in between page refreshes
            let userSession = new User()
            let data : any = user;
            let keyObj : any = JSON.parse(localStorage.getItem('key'));
            userSession.id = data.pk;
            userSession.lastName = data.last_name;
            userSession.firstName = data.first_name;
            userSession.email = data.email;
            userSession.token = keyObj.key;
            localStorage.setItem('user', JSON.stringify(userSession));
            this.userSubject.next(userSession);
            return user;
        }));
    }

    logout() {
        // remove user from local storage and set current user to null
        localStorage.removeItem('user');
        localStorage.removeItem('key');
        this.userSubject.next(null);
        this.router.navigate(['/login']);
    }

    register(user: any) {
        return this.http.post(`${environment.apiUrl}/rest-auth/registration/`, user);
    }

    getAll() {
        return this.http.get<User[]>(`${environment.apiUrl}/users`);
    }

    getById(id: string) {
        return this.http.get<User>(`${environment.apiUrl}/users/${id}`);
    }

    update(id, params) {
        return this.http.put(`${environment.apiUrl}/users/${id}`, params)
            .pipe(map(x => {
                // update stored user if the logged in user updated their own record
                if (id == this.userValue.id) {
                    // update local storage
                    const user = { ...this.userValue, ...params };
                    localStorage.setItem('user', JSON.stringify(user));

                    // publish updated user to subscribers
                    this.userSubject.next(user);
                }
                return x;
            }));
    }

    delete(id: string) {
        return this.http.delete(`${environment.apiUrl}/users/${id}`)
            .pipe(map(x => {
                // auto logout if the logged in user deleted their own record
                if (id == this.userValue.id) {
                    this.logout();
                }
                return x;
            }));
    }

    getCountries() {
        return this.http.get('/assets/codes/countries.json');
    }
}