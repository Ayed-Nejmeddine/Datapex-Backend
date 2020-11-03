import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { BehaviorSubject, Observable, forkJoin } from 'rxjs';
import { catchError, map } from 'rxjs/operators';


import { environment } from '../../environments/environment';
import { Profile, User, Document } from '../_models';

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
        return this.http.get<Document>(`${environment.apiUrl}/api/v1/upload-document/${id}/`);
    }

    launchSemanticAnalyse(document : Document){
        return this.fetchOutput(`${environment.apiUrl}/api/v1/upload-document/${document.id}/launch-semantic-analysis/`)
    }

    launchSyntacticAnalyse(document : Document){
        return this.http.get(`${environment.apiUrl}/api/v1/upload-document/${document.id}/launch-syntactic-analysis/`);
    }

    getSyntacticAnalysisResults(document : Document){
        return this.fetchOutput(`${environment.apiUrl}/api/v1/upload-document/${document.id}/get-syntactic-analysis-results/`)
    }

    getLinksBetweenColumns(document : Document){
        return this.fetchOutput(`${environment.apiUrl}/api/v1/upload-document/${document.id}/get-links-between-columns/`)
    }

    fetchOutput(url): Observable<ArrayBuffer> {
        let headers = new HttpHeaders();
        const options: {
            headers?: HttpHeaders;
            observe?: 'body';
            params?: HttpParams;
            reportProgress?: true;
            responseType: 'arraybuffer';
            withCredentials?: true;
        } = {
            responseType: 'arraybuffer'
        };
    
        return this.http
            .get(url, options)
            .pipe(
                map((file: ArrayBuffer) => {
                    return file;
                })
            );
    }

    
}