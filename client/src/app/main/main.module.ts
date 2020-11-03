import { NgModule } from '@angular/core';
import { ReactiveFormsModule } from '@angular/forms';
import { CommonModule, DatePipe } from '@angular/common';

import { MainRoutingModule } from './main-routing.module';
import { LayoutComponent } from './layout.component';
import { ProfileComponent } from './profile.component';
import { DefaultComponent } from './default.component';

import { FormsModule } from '@angular/forms';
import { MatInputModule } from '@angular/material/input';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap'

import { MatIconModule } from '@angular/material/icon';
import { MatAutocompleteModule } from '@angular/material/autocomplete';
import { MatButtonModule } from '@angular/material/button';
import { MatButtonToggleModule } from '@angular/material/button-toggle';
import { MatCardModule } from '@angular/material/card';
import { MatCheckboxModule } from '@angular/material/checkbox';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatProgressBarModule } from '@angular/material/progress-bar';
import { FormProfileComponent } from './form-profile/form-profile.component';
import { FormInfosComponent } from './form-infos/form-infos.component';
import { VerifyChangeAccountComponent } from './form-infos/verify-account/verify-change-account.component';
import { FormLanguageComponent } from './form-language/form-language.component';
import { ImageCropperModule } from 'ngx-image-cropper';
import { HighlightDirective } from '@app/_directives/highlight.directive';

@NgModule({
    imports: [
        CommonModule,
        ReactiveFormsModule,
        MainRoutingModule,
        FormsModule,
        NgbModule,
        MatInputModule,
        MatIconModule,
        MatAutocompleteModule,
        MatButtonModule,
        MatButtonToggleModule,
        MatCardModule,
        MatCheckboxModule,
        MatFormFieldModule,
        MatProgressBarModule,
        ImageCropperModule,
    ],
    declarations: [
        LayoutComponent,
        ProfileComponent,
        DefaultComponent,
        FormProfileComponent,
        FormInfosComponent,
        FormLanguageComponent,
        VerifyChangeAccountComponent,
        HighlightDirective
    ],
    exports: [HighlightDirective],
    providers: [
        DatePipe,
    ]
})
export class MainModule { }