import { NgModule } from "@angular/core";
import { Routes, RouterModule } from "@angular/router";
import { LoginComponent } from "./login/login.component";
import { UserComponent } from "./user/user.component";
import { HomeComponent } from "./home/home.component";
import { NotfoundComponent } from './notfound/notfound.component';
import { ScrumboardComponent } from './scrumboard/scrumboard.component';
import { DragulaModule } from 'ng2-dragula';




const routes: Routes = [
  { path: "", redirectTo: "/home", pathMatch: "full" },
  { path: "home", component: HomeComponent },
  { path: "login", component: LoginComponent },
  { path: "user", component: UserComponent },
  { path: 'scrumboard', component: ScrumboardComponent},
  {path: '**', component: NotfoundComponent }

];

@NgModule({
  imports: [RouterModule.forRoot(routes), DragulaModule],
  exports: [RouterModule]
})
export class AppRoutingModule {}