import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { Router } from '@angular/router';
import { AuthService } from '../../core/auth/auth.service';

@Component({
  selector: 'app-unauthorized',
  standalone: true,
  imports: [CommonModule, MatCardModule, MatButtonModule, MatIconModule],
  template: `
    <div class="unauthorized-container">
      <mat-card class="error-card">
        <mat-card-header>
          <i class="fas fa-lock error-icon"></i>
          <mat-card-title>Access Denied</mat-card-title>
          <mat-card-subtitle>You don't have permission to access this resource</mat-card-subtitle>
        </mat-card-header>
        <mat-card-content>
          <p>Sorry, you don't have the required permissions to view this page.</p>
          <p>Please contact an administrator if you believe this is an error.</p>
        </mat-card-content>
        <mat-card-actions>
          <button mat-raised-button color="primary" (click)="goHome()">
            <i class="fas fa-home"></i>
            Go to Dashboard
          </button>
          <button mat-raised-button (click)="login()">
            <i class="fas fa-sign-in-alt"></i>
            Login Again
          </button>
        </mat-card-actions>
      </mat-card>
    </div>
  `,
  styles: [`
    .unauthorized-container {
      display: flex;
      justify-content: center;
      align-items: center;
      min-height: 80vh;
      padding: 20px;
    }

    .error-card {
      max-width: 500px;
      text-align: center;
    }

    .error-icon {
      font-size: 48px;
      color: #f44336;
      margin-bottom: 16px;
    }

    mat-card-actions {
      display: flex;
      justify-content: center;
      gap: 16px;
      margin-top: 20px;
    }

    i {
      margin-right: 8px;
    }
  `]
})
export class UnauthorizedComponent {
  constructor(
    private router: Router,
    private authService: AuthService
  ) {}

  goHome(): void {
    this.router.navigate(['/dashboard']);
  }

  login(): void {
    this.authService.login();
  }
}