import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { TranslateLoader } from '@ngx-translate/core';
import { Observable, of } from 'rxjs';


@Injectable({ providedIn: 'root' })
export class CustomLoader implements TranslateLoader {
    constructor(private http: HttpClient) {
    }
    getTranslation(lang: string): Observable<any> {
        return this.http.get(`/assets/i18n/${lang}.json`);
    }
}

