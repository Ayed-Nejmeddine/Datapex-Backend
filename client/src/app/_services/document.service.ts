import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable, forkJoin } from 'rxjs';
import { catchError, map } from 'rxjs/operators';

import { environment } from '../../environments/environment';
import { Profile, User } from '../_models';

@Injectable({ providedIn: 'root' })
export class DocumentService {
  
    constructor(
        private router: Router,
        private http: HttpClient
    ) {

    }
    getAll() {
        return this.http.get<User[]>(`${environment.apiUrl}/api/v1/upload-document/`);
    }

    getById(id: number) {
        return this.http.get<User>(`${environment.apiUrl}/api/v1/upload-document/${id}/`);
    }

    
}