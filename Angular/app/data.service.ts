import { Injectable } from '@angular/core';
import {HttpClient,HttpHeaders} from '@angular/common/http';
import { Router } from '@angular/router';

// const httpOptions = {
//   headers: new HttpHeaders({
//     'Content-Type':  'application/json',
//     'Authorization': 'my-auth-token'
//   })
// };

@Injectable({
  providedIn: 'root'
})
export class DataService {

  public domain_name = '127.0.0.1:8000';


  public username;
  public password;
  

  public login_username;
  public login_password;

  public role;
  public users;
  public goal_name;
  public goal_id;
  public to_id;
  public fullname;
  public authOptions;
  public id;

  public message;
  public user_fullname = '';
  public user_username;
  public user_email;
  public user_password;
  public user_password_repeat;  
  public user_usertype;
  public httpOptions = {
    headers: new HttpHeaders({'Content-Type': 'application/json'})
  };
  

  constructor(private http: HttpClient, private router: Router,) { }
  user()
  {
    this.http.post('http://' + this.domain_name + '/samsonadejoroscrumy/api/scrumusers/', JSON.stringify({'username':this.user_username,'email': this.user_email,  'password': this.user_password,'pass_auth':this.user_password_repeat, 'full_name': this.user_fullname,'usertype': this.user_usertype}), this.httpOptions).subscribe(
        data => {
            this.message = 'You have Signed Up Successfully!';
            this.user_fullname = '';
            this.user_username = '';
            // this.router.navigate(['scrumboard']);
            this.user_email = '';
            this.user_password = '';
            this.user_password_repeat = '';
            this.user_usertype = '';
        },
        err => {
          this.message = 'User Creation Failed! Unexpected Error!';
          console.error(err);
          this.user_fullname = '';
          // this.user_lastname = '';
          this.user_username = '';
          this.user_email = '';
          this.user_password = '';
          this.user_password_repeat = '';
          this.user_usertype = '';

      }
    );
  }
  
  login()
  {
    this.http.post('http://' + this.domain_name + '/samsonadejoroscrumy/api-token-auth/', JSON.stringify({'username': this.login_username, 'password': this.login_password}), this.httpOptions).subscribe(
      data => {
        
        
        
        
        
        sessionStorage.setItem('username', this.login_username);
        sessionStorage.setItem('role', data['role']);
        sessionStorage.setItem('token', data['token'])
        this.username = this.login_username;
        this.password = this.login_password;
        //this.fullname = data['nickname'];
        this.users = data['data'];
        this.role = data['role'];
        this.router.navigate(['scrumboard']);
        //this.role = '';
        this.login_username = '';
        this.login_password = '';
        console.log(data);

        this.authOptions = {
          headers: new HttpHeaders({'Content-Type': 'application/json', 'Authorization': 'JWT ' + data['token']})
        };
      },
      err => {
        if(err['status'] == 400)
            this.message = 'Login Failed: Invalid Credentials.';
        else
            this.message = 'Login Failed! Unexpected Error!';
    console.error(err);
    this.username = '';
    this.password = '';
    
    this.login_username = '';
    this.login_password = '';   
    }
    )
  }
  logout ()
  {
  this.username = '';
  this.password= '';
  this.role = '';
  // this.role_id = '';
  this.users = [];
  this.message = 'Thank You for Using Scrum'
  // this.realname = '';
  // this.project = 0;
  // this.project_name = '';

  this.authOptions = {};
  sessionStorage.removeItem('username');
  sessionStorage.removeItem('role');
  this.router.navigate(['login']);
  // sessionStorage.removeItem('role_id');
  // sessionStorage.removeItem('token');
  // sessionStorage.removeItem('project_id');
  // sessionStorage.removeItem('realname');

  }
  addGoal(){
    this.http.post('http://' + this.domain_name + '/samsonadejoroscrumy/api/goals/', JSON.stringify({'username': this.username, 'password': this.password, 'name':this.goal_name, 'id': this.goal_id}), this.httpOptions).subscribe(
    data => {
      if(data['exit'] == 0)
        this.users = data['data'];
        this.message = data['message'];
        this.goal_name = '';
        this.goal_id = '';
    },
    err =>{
      console.error(err);
      this.message = "Unexpected Error";
      this.goal_name = '';
      this.goal_id='';
    }
    );
  }
  moveGoal(goal_id, to_id){
    this.http.patch('http://' + this.domain_name + '/samsonadejoroscrumy/api/goals/', JSON.stringify({'username': this.username, 'password': this.password, 'goal_id':goal_id, 'to_id': to_id, }), this.httpOptions).subscribe(
    data => {
      if(data['exit'] == 0)
        this.users = data['data'];
        this.message = data['message'];
    },
    err =>{
      console.error(err);
      this.message = "Unexpected Error!";
    }
    );
  }

  changeOwner(from_id, to_id, goal_id){
  this.http.put('http://' + this.domain_name + '/samsonadejoroscrumy/api/goals/', JSON.stringify({'username': this.username, 'password': this.password,'mode': 0, 'from_id':from_id, 'to_id': to_id }), this.httpOptions).subscribe(
    data => {
      if(data['exit'] == 0)
        this.users = data['data'];
        this.message = data['message'];
    },
    err =>{
      console.error(err);
      this.message ="Unexpected Error!";
    }
    );

  }

}