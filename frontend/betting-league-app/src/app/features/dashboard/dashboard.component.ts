import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { AuthService } from '../../core/auth/auth.service';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule, MatCardModule, MatButtonModule, MatIconModule],
  template: `
    <div class="dashboard-container">
      <mat-card class="welcome-card">
        <mat-card-header>
          <mat-card-title>Welcome to Betting League Championship</mat-card-title>
          <mat-card-subtitle>Your personalized betting dashboard</mat-card-subtitle>
        </mat-card-header>
        <mat-card-content>
          <p>Hello, {{ currentUser?.username || 'User' }}!</p>
          <p>Ready to place some bets and compete in the championship?</p>
        </mat-card-content>
        <mat-card-actions>
          <button mat-raised-button color="primary">
            <mat-icon>sports_soccer</mat-icon>
            View Active Bets
          </button>
          <button mat-raised-button color="accent">
            <mat-icon>leaderboard</mat-icon>
            Championship Standings
          </button>
        </mat-card-actions>
      </mat-card>

      <div class="dashboard-grid">
        <mat-card class="stats-card">
          <mat-card-header>
            <mat-card-title>Your Stats</mat-card-title>
          </mat-card-header>
          <mat-card-content>
            <p>Total Bets: 0</p>
            <p>Wins: 0</p>
            <p>Win Rate: 0%</p>
            <p>Current Ranking: -</p>
          </mat-card-content>
        </mat-card>

        <mat-card class="recent-activity-card">
          <mat-card-header>
            <mat-card-title>Recent Activity</mat-card-title>
          </mat-card-header>
          <mat-card-content>
            <p>No recent activity</p>
          </mat-card-content>
        </mat-card>
      </div>
    </div>
  `,
  styles: [`
    .dashboard-container {
      padding: 20px;
      max-width: 1200px;
      margin: 0 auto;
    }

    .welcome-card {
      margin-bottom: 20px;
    }

    .dashboard-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
      gap: 20px;
    }

    .stats-card, .recent-activity-card {
      height: fit-content;
    }

    mat-card-actions {
      display: flex;
      gap: 10px;
    }

    mat-icon {
      margin-right: 8px;
    }
  `]
})
export class DashboardComponent {
  currentUser: any = null;

  constructor(private authService: AuthService) {
    this.currentUser = this.authService.getCurrentUser();
  }
}