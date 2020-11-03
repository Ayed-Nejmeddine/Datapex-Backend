import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { ReactiveFormsModule } from '@angular/forms';
import { HttpClient, HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';

import { AppRoutingModule } from './app-routing.module';
import { TokenInterceptor, ErrorInterceptor } from './_helpers';
import { AppComponent } from './app.component';
import { AlertComponent } from './_components';
import { HomeComponent } from './home';;
import { BrowserAnimationsModule } from '@angular/platform-browser/animations'
    ;
import { NgbModule } from '@ng-bootstrap/ng-bootstrap'

import { FormsModule } from '@angular/forms';
import { MatInputModule } from '@angular/material/input';

import { MatIconModule } from '@angular/material/icon';
import { MatAutocompleteModule } from '@angular/material/autocomplete';
import { MatButtonModule } from '@angular/material/button';
import { MatButtonToggleModule } from '@angular/material/button-toggle';
import { MatCardModule } from '@angular/material/card';
import { MatCheckboxModule } from '@angular/material/checkbox';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MainModule } from './main/main.module';
import { TranslateHttpLoader } from '@ngx-translate/http-loader';

import { TranslateModule, TranslateLoader } from '@ngx-translate/core';
import { CustomLoader } from './_services';;
export function createTranslateLoader(httpClient: HttpClient) {
    return new CustomLoader(httpClient);
}

@NgModule({
    imports: [
        BrowserModule,
        ReactiveFormsModule,
        FormsModule,
        HttpClientModule,
        AppRoutingModule,
        NgbModule,
        BrowserAnimationsModule,
        MatInputModule,
        MatIconModule,
        MatAutocompleteModule,
        MatButtonModule,
        MatButtonToggleModule,
        MatCardModule,
        MatCheckboxModule,
        MatFormFieldModule,
        MainModule,
        TranslateModule.forRoot({
            loader: {
                provide: TranslateLoader,
                useFactory: (createTranslateLoader),
                deps: [HttpClient]
            }
        }),
    ],
    declarations: [
        AppComponent,
        AlertComponent,
        HomeComponent
        ],
    providers: [
        { provide: HTTP_INTERCEPTORS, useClass: TokenInterceptor, multi: true },
        { provide: HTTP_INTERCEPTORS, useClass: ErrorInterceptor, multi: true },
    ],
    bootstrap: [AppComponent]
})
export class AppModule { };