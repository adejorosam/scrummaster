import { Component, OnInit } from '@angular/core';
import { Routes, RouterModule, Router } from '@angular/router';
import { DataService } from './../data.service';

@Component({
  selector: 'app-user',
  templateUrl: './user.component.html',
  styleUrls: ['./user.component.css']
})
export class UserComponent implements OnInit {

  constructor(private router: Router, private dataservice: DataService ) { }

  ngOnInit() {
  }
  signup() {
    this.dataservice.user();
  }
  toLogin()
  {
    this.router.navigate(['login']);
    this.dataservice.message = '';
  }
  
}


