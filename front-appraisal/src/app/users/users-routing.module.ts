import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { CreateAccountComponent } from './create-account/create-account.component';
import { ForgotPasswordComponent } from './forgot-password/forgot-password.component';
import { LoginComponent } from './login/login.component';
import { UsersComponent } from './users.component';

const routes: Routes = [
  {
      path: '', component: UsersComponent,
      children: [
          { path: 'login', component: LoginComponent },
          { path: 'create-account', component: CreateAccountComponent },
          { path: 'forgot-password', component: ForgotPasswordComponent }
      ]
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class UsersRoutingModule { }
