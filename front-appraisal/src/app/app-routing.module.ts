import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';
import { Routes, RouterModule, PreloadAllModules } from '@angular/router';
import { AuthGuard } from './_helpers/auth.guard';


const usersModule = () => import('./users/users.module').then(x => x.UsersModule);
const mainModule = () => import('./main/main.module').then(x => x.MainModule);


const routes: Routes = [
  { path: 'users', loadChildren: usersModule },
  { path: 'main', loadChildren: mainModule, canActivate: [AuthGuard] },
  { path: '',   redirectTo: '/main', pathMatch: 'full' },
  { path: '**', redirectTo: '' },  // Wildcard route for a 404 page
];


@NgModule({
  imports: [RouterModule.forRoot(routes, { useHash: true, preloadingStrategy: PreloadAllModules })],
  exports: [RouterModule]
})
export class AppRoutingModule { }
