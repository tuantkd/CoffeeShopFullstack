import { Component, OnInit } from '@angular/core';
import { AuthService } from '../../services/auth.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-user-page',
  templateUrl: './user-page.page.html',
  styleUrls: ['./user-page.page.scss'],
})
export class UserPagePage implements OnInit {
  loginURL: string;

  constructor(
    public auth: AuthService,
    private router: Router
  ) {
    this.loginURL = auth.build_login_link('/tabs/user-page');
  }

  ngOnInit() {
  }

  logout() {
    this.auth.logout();
    this.router.navigate(['/tabs/user-page']);
  }

}
