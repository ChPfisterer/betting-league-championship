import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { Router } from '@angular/router';

@Component({
  selector: 'app-not-found',
  standalone: true,
  imports: [CommonModule, MatCardModule, MatButtonModule, MatIconModule],
  template: `
    <div class="not-found-container">
      <mat-card class="error-card">
        <mat-card-header>
          <mat-icon class="error-icon">search_off</mat-icon>
          <mat-card-title>404 - Page Not Found</mat-card-title>
          <mat-card-subtitle>The page you're looking for doesn't exist</mat-card-subtitle>
        </mat-card-header>
        <mat-card-content>
          <p>Sorry, we couldn't find the page you were looking for.</p>
          <p>It might have been moved, deleted, or you entered the wrong URL.</p>
        </mat-card-content>
        <mat-card-actions>
          <button mat-raised-button color="primary" (click)="goHome()">
            <mat-icon>home</mat-icon>
            Go to Dashboard
          </button>
          <button mat-raised-button (click)="goBack()">
            <mat-icon>arrow_back</mat-icon>
            Go Back
          </button>
        </mat-card-actions>
      </mat-card>
    </div>
  `,
  styles: [`
    .not-found-container {
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
      color: #ff9800;
      margin-bottom: 16px;
    }

    mat-card-actions {
      display: flex;
      justify-content: center;
      gap: 16px;
      margin-top: 20px;
    }

    mat-icon {
      margin-right: 8px;
    }
  `]
})
export class NotFoundComponent {
  constructor(private router: Router) {}

  goHome(): void {
    this.router.navigate(['/dashboard']);
  }

  goBack(): void {
    window.history.back();
  }
}