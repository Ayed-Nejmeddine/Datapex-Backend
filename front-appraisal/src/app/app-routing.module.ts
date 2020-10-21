import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { CreateAccountComponent } from './account/create-account/create-account.component';
import { ForgotPasswordComponent } from './account/forgot-password/forgot-password.component';
import { LoginComponent } from './account/login/login.component';
import { MainPageComponent } from './dashboard/main-page/main-page.component';
import { AuthGuard } from './_helpers/auth.guard';

const routes: Routes = [
  { path:  '', redirectTo:  'dashboard', pathMatch:  'full', canActivate: [AuthGuard] },
  {
    path: 'dashboard',
    component: MainPageComponent, canActivate: [AuthGuard]
  },
  {
    path: 'create-account',
    component: CreateAccountComponent
  },
  {
    path: 'login',
    component: LoginComponent
  },
  {
    path: 'forgot-password',
    component: ForgotPasswordComponent
  },
  { path: '**', redirectTo: '' }
];


@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
