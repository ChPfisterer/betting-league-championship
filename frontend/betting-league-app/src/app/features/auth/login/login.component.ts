import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatSnackBarModule, MatSnackBar } from '@angular/material/snack-bar';
import { Router } from '@angular/router';
import { AuthService } from '../../../core/auth/auth.service';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [
    CommonModule,
    MatCardModule, 
    MatButtonModule, 
    MatIconModule, 
    MatProgressSpinnerModule,
    MatSnackBarModule
  ],
  template: `
    <div class="login-container">
      <mat-card class="login-card">
        <mat-card-header>
          <div class="login-header">
            <mat-icon class="login-icon">sports_soccer</mat-icon>
            <mat-card-title>Betting League Championship</mat-card-title>
            <mat-card-subtitle>Secure Authentication via Keycloak</mat-card-subtitle>
          </div>
        </mat-card-header>

        <mat-card-content>
          <div class="welcome-section">
            <h3>Welcome to the Championship!</h3>
            <p>Experience secure, enterprise-grade authentication powered by Keycloak.</p>
            
            <div class="features-list">
              <div class="feature-item">
                <mat-icon color="primary">security</mat-icon>
                <span>Enterprise-grade security</span>
              </div>
              <div class="feature-item">
                <mat-icon color="primary">verified_user</mat-icon>
                <span>Single Sign-On (SSO)</span>
              </div>
              <div class="feature-item">
                <mat-icon color="primary">group</mat-icon>
                <span>Centralized user management</span>
              </div>
              <div class="feature-item">
                <mat-icon color="primary">sports_soccer</mat-icon>
                <span>Access to betting platform</span>
              </div>
            </div>
          </div>

          <div class="auth-actions">
            <button mat-raised-button 
                    color="primary" 
                    class="auth-button login-btn"
                    (click)="loginWithKeycloak()"
                    [disabled]="isLoading">
              <mat-spinner diameter="20" *ngIf="isLoading && authAction === 'login'"></mat-spinner>
              <mat-icon *ngIf="!isLoading">login</mat-icon>
              <span *ngIf="!isLoading">Sign In</span>
              <span *ngIf="isLoading && authAction === 'login'">Redirecting...</span>
            </button>

            <button mat-stroked-button 
                    color="primary" 
                    class="auth-button register-btn"
                    (click)="registerWithKeycloak()"
                    [disabled]="isLoading">
              <mat-spinner diameter="20" *ngIf="isLoading && authAction === 'register'"></mat-spinner>
              <mat-icon *ngIf="!isLoading">person_add</mat-icon>
              <span *ngIf="!isLoading">Create Account</span>
              <span *ngIf="isLoading && authAction === 'register'">Redirecting...</span>
            </button>
          </div>

          <div class="info-section">
            <mat-icon class="info-icon">info</mat-icon>
            <p class="info-text">
              You'll be securely redirected to our Keycloak authentication service. 
              Your credentials are never stored on our platform.
            </p>
          </div>
        </mat-card-content>
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
      width: 100%;
      max-width: 450px;
      box-shadow: 0 8px 32px rgba(0,0,0,0.1);
      border-radius: 16px;
    }

    .login-header {
      text-align: center;
      padding: 20px 0;
    }

    .login-icon {
      font-size: 48px;
      width: 48px;
      height: 48px;
      color: #667eea;
      margin-bottom: 16px;
    }

    .welcome-section {
      text-align: center;
      margin: 20px 0;
    }

    .welcome-section h3 {
      color: #333;
      margin-bottom: 12px;
      font-weight: 600;
    }

    .welcome-section p {
      color: #666;
      margin-bottom: 24px;
      line-height: 1.5;
    }

    .features-list {
      margin: 24px 0;
      text-align: left;
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
    }

    .auth-actions {
      display: flex;
      flex-direction: column;
      gap: 16px;
      margin: 32px 0;
    }

    .auth-button {
      width: 100%;
      height: 56px;
      font-size: 16px;
      font-weight: 500;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
    }

    .login-btn {
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white;
      border: none;
    }

    .register-btn {
      border: 2px solid #667eea;
      color: #667eea;
    }

    .register-btn:hover {
      background-color: rgba(102, 126, 234, 0.1);
    }

    .info-section {
      display: flex;
      align-items: flex-start;
      gap: 12px;
      padding: 16px;
      background-color: #f8f9fa;
      border-radius: 8px;
      margin-top: 24px;
    }

    .info-icon {
      color: #666;
      font-size: 20px;
      margin-top: 2px;
    }

    .info-text {
      color: #666;
      font-size: 14px;
      line-height: 1.4;
      margin: 0;
    }

    mat-spinner {
      margin-right: 8px;
    }
  `]
})
export class LoginComponent implements OnInit {
  isLoading = false;
  authAction: 'login' | 'register' | null = null;

  constructor(
    private authService: AuthService,
    private router: Router,
    private snackBar: MatSnackBar
  ) {}

  ngOnInit(): void {
    // Redirect if already authenticated
    this.authService.isAuthenticated$.subscribe(isAuth => {
      if (isAuth) {
        this.router.navigate(['/dashboard']);
      }
    });
  }

  loginWithKeycloak(): void {
    if (!this.isLoading) {
      this.isLoading = true;
      this.authAction = 'login';
      
      try {
        this.authService.initiateKeycloakLogin();
        // The user will be redirected to Keycloak, so we don't need to handle the response here
      } catch (error) {
        this.isLoading = false;
        this.authAction = null;
        console.error('Keycloak login error:', error);
        this.snackBar.open('Failed to redirect to Keycloak. Please try again.', 'Close', {
          duration: 5000
        });
      }
    }
  }

  registerWithKeycloak(): void {
    if (!this.isLoading) {
      this.isLoading = true;
      this.authAction = 'register';
      
      try {
        // For Keycloak, we can use the same login flow with a registration parameter
        // or redirect directly to Keycloak's registration page
        this.authService.initiateKeycloakRegistration();
      } catch (error) {
        this.isLoading = false;
        this.authAction = null;
        console.error('Keycloak registration error:', error);
        this.snackBar.open('Failed to redirect to Keycloak registration. Please try again.', 'Close', {
          duration: 5000
        });
      }
    }
  }
}