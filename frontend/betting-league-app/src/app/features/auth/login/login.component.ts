import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { Router } from '@angular/router';
import { AuthService } from '../../../core/auth/auth.service';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, MatCardModule, MatButtonModule, MatIconModule, MatProgressSpinnerModule],
  template: `
    <div class="login-container">
      <mat-card class="login-card">
        <mat-card-header>
          <div class="logo-section">
            <mat-icon class="logo-icon">sports_soccer</mat-icon>
            <mat-card-title>Betting League Championship</mat-card-title>
          </div>
          <mat-card-subtitle>Sign in to your account</mat-card-subtitle>
        </mat-card-header>
        
        <mat-card-content>
          <div class="welcome-text">
            <p>Welcome to the ultimate sports betting championship platform!</p>
            <p>Sign in to place bets, compete with other players, and climb the leaderboard.</p>
          </div>

          <div class="features-list">
            <div class="feature-item">
              <mat-icon color="primary">check_circle</mat-icon>
              <span>Place bets on your favorite sports</span>
            </div>
            <div class="feature-item">
              <mat-icon color="primary">check_circle</mat-icon>
              <span>Compete in championships</span>
            </div>
            <div class="feature-item">
              <mat-icon color="primary">check_circle</mat-icon>
              <span>Track your performance</span>
            </div>
            <div class="feature-item">
              <mat-icon color="primary">check_circle</mat-icon>
              <span>Real-time leaderboards</span>
            </div>
          </div>
        </mat-card-content>

        <mat-card-actions>
          <button 
            mat-raised-button 
            color="primary" 
            class="login-button"
            (click)="loginWithKeycloak()"
            [disabled]="isLoading">
            <mat-spinner *ngIf="isLoading" diameter="20" class="button-spinner"></mat-spinner>
            <mat-icon *ngIf="!isLoading">login</mat-icon>
            {{ isLoading ? 'Redirecting...' : 'Sign In with Keycloak' }}
          </button>
          
          <div class="login-info">
            <p>
              <mat-icon>info</mat-icon>
              You'll be redirected to our secure login page
            </p>
          </div>
        </mat-card-actions>
      </mat-card>
    </div>
  `,
  styles: [`
    .login-container {
      display: flex;
      justify-content: center;
      align-items: center;
      min-height: 100vh;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      padding: 20px;
    }

    .login-card {
      max-width: 500px;
      width: 100%;
      padding: 20px;
      box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
      backdrop-filter: blur(10px);
    }

    .logo-section {
      display: flex;
      align-items: center;
      justify-content: center;
      flex-direction: column;
      margin-bottom: 16px;
    }

    .logo-icon {
      font-size: 48px;
      height: 48px;
      width: 48px;
      color: #3f51b5;
      margin-bottom: 8px;
    }

    mat-card-title {
      text-align: center;
      color: #333;
      font-weight: 600;
    }

    mat-card-subtitle {
      text-align: center;
      margin-top: 8px;
    }

    .welcome-text {
      text-align: center;
      margin: 24px 0;
      color: #666;
      line-height: 1.5;
    }

    .features-list {
      margin: 24px 0;
    }

    .feature-item {
      display: flex;
      align-items: center;
      margin: 12px 0;
      color: #555;
    }

    .feature-item mat-icon {
      margin-right: 12px;
      font-size: 20px;
      height: 20px;
      width: 20px;
    }

    .login-button {
      width: 100%;
      height: 48px;
      font-size: 16px;
      font-weight: 500;
      margin-bottom: 16px;
      position: relative;
    }

    .button-spinner {
      margin-right: 8px;
    }

    .login-info {
      text-align: center;
      color: #666;
      font-size: 14px;
    }

    .login-info mat-icon {
      font-size: 16px;
      height: 16px;
      width: 16px;
      margin-right: 4px;
      vertical-align: middle;
    }

    mat-card-actions {
      padding: 16px 0 0 0;
    }
  `]
})
export class LoginComponent {
  isLoading = false;

  constructor(
    private authService: AuthService,
    private router: Router
  ) {
    // Check if user is already authenticated
    this.authService.isAuthenticated$.subscribe((isAuthenticated: boolean) => {
      if (isAuthenticated) {
        this.redirectAfterLogin();
      }
    });
  }

  loginWithKeycloak(): void {
    this.isLoading = true;
    this.authService.login();
  }

  private redirectAfterLogin(): void {
    const redirectUrl = sessionStorage.getItem('redirectUrl') || '/dashboard';
    sessionStorage.removeItem('redirectUrl');
    this.router.navigate([redirectUrl]);
  }
}