import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { LayoutComponent } from './layout.component';
import { ProfileComponent } from './profile.component';
import { DefaultComponent } from './default.component';
import { DocumentComponent } from './document/document.component';

const routes: Routes = [
    {
        path: '', component: LayoutComponent,
        children: [
            { path: '', component: DefaultComponent },
            { path: 'profile', component: ProfileComponent },
            { path: 'document/:id', component: DocumentComponent },
        ]
    }
];

@NgModule({
    imports: [RouterModule.forChild(routes)],
    exports: [RouterModule]
})
export class MainRoutingModule { }