import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterOutlet, Router } from '@angular/router';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatMenuModule } from '@angular/material/menu';
import { MatDividerModule } from '@angular/material/divider';
// import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { AuthService } from './core/auth/auth.service';
import { FontAwesomeService } from './core/services/fontawesome.service';

@Component({
  selector: 'app-root',
  imports: [
    CommonModule,
    RouterOutlet,
    MatToolbarModule,
    MatButtonModule,
    MatIconModule,
    MatMenuModule,
    MatDividerModule
  ],
  templateUrl: './app.component.html',
  styleUrl: './app.scss'
})
export class App implements OnInit {
  title = 'Betting League Championship';
  
  constructor(
    private authService: AuthService,
    private router: Router,
    private fontAwesomeService: FontAwesomeService
  ) {}

  ngOnInit(): void {
    // Load FontAwesome kit dynamically
    this.fontAwesomeService.loadFontAwesome().catch(error => {
      console.warn('FontAwesome failed to load, using fallback styling:', error);
    });
  }

  get isAuthenticated$() {
    return this.authService.isAuthenticated$;
  }

  get currentUser$() {
    return this.authService.currentUser$;
  }

  viewProfile(): void {
    this.router.navigate(['/profile']);
  }

  viewBettingHistory(): void {
    // TODO: Navigate to betting history
    console.log('Navigate to betting history');
  }

  viewSettings(): void {
    // TODO: Navigate to settings
    console.log('Navigate to settings');
  }

  logout(): void {
    console.log('App: Starting logout...');
    this.authService.logout().subscribe({
      next: () => {
        console.log('App: Logout initiated (Keycloak will handle redirect)');
        // Note: No manual navigation needed, Keycloak will redirect back to login
      },
      error: (error) => {
        console.error('App: Logout error:', error);
        // Fallback: redirect to login if something goes wrong
        this.router.navigate(['/login']);
      }
    });
  }
}
