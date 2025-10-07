import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterOutlet } from '@angular/router';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { AuthService } from './core/auth/auth.service';

@Component({
  selector: 'app-root',
  imports: [
    CommonModule,
    RouterOutlet,
    MatToolbarModule,
    MatButtonModule,
    MatIconModule
  ],
  templateUrl: './app.component.html',
  styleUrl: './app.scss'
})
export class App {
  title = 'Betting League Championship';
  
  constructor(private authService: AuthService) {}

  get isAuthenticated$() {
    return this.authService.isAuthenticated$;
  }

  get currentUser$() {
    return this.authService.currentUser$;
  }

  logout(): void {
    this.authService.logout().subscribe();
  }
}
