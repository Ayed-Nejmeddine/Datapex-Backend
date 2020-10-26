import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms'; 
import { ReactiveFormsModule } from '@angular/forms';
import { UsersRoutingModule } from './users-routing.module';
import { UsersComponent } from './users.component';
import { ForgotPasswordComponent } from './forgot-password/forgot-password.component';
import { CreateAccountComponent } from './create-account/create-account.component';
import { LoginComponent } from './login/login.component';
import { FormSmsComponent } from './forgot-password/forms/form-sms/form-sms.component';
import { FormCodeComponent } from './forgot-password/forms/form-code/form-code.component';
import { FormReinitializeComponent } from './forgot-password/forms/form-reinitialize/form-reinitialize.component';
import { VerifyAccountComponent } from './create-account/verify-account/verify-account.component';
import {MatInputModule} from '@angular/material/input';

import {MatIconModule} from '@angular/material/icon';
import {MatAutocompleteModule} from '@angular/material/autocomplete';
import {MatButtonModule} from '@angular/material/button';
import {MatButtonToggleModule} from '@angular/material/button-toggle';
import {MatCardModule} from '@angular/material/card';
import {MatCheckboxModule} from '@angular/material/checkbox';
import {MatFormFieldModule} from '@angular/material/form-field';
@NgModule({
  declarations: [
    UsersComponent,
    CreateAccountComponent,
    LoginComponent,
    ForgotPasswordComponent,
    FormSmsComponent,
    FormCodeComponent,
    FormReinitializeComponent,
    VerifyAccountComponent,
  ],
  imports: [
    CommonModule,
    UsersRoutingModule,
    MatInputModule,
    MatIconModule,
    MatAutocompleteModule,
    MatButtonModule,
    MatButtonToggleModule,
    MatCardModule,
    MatCheckboxModule,
    MatFormFieldModule,
    MatAutocompleteModule,
    FormsModule,
    ReactiveFormsModule,
  ]
})
export class UsersModule { }
