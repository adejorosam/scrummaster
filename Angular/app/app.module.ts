import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';

import { DataService } from './data.service';
import { FormsModule } from '@angular/forms';
import { from } from 'rxjs';

import { HttpClientModule } from '@angular/common/http';
import { LoginComponent } from './login/login.component';
import { UserComponent } from './user/user.component';
import { HomeComponent } from './home/home.component';
import { NotfoundComponent } from './notfound/notfound.component';
import { ScrumboardComponent } from './scrumboard/scrumboard.component';
import { DragulaModule } from 'ng2-dragula';





@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,
    UserComponent,
    HomeComponent,
    NotfoundComponent,
    ScrumboardComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    FormsModule,
    DragulaModule.forRoot()

    
  ],
  providers: [DataService],
  bootstrap: [AppComponent]
})
export class AppModule { }
