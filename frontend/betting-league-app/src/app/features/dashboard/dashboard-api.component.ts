import { Component, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatTabsModule } from '@angular/material/tabs';
import { MatChipsModule } from '@angular/material/chips';
import { MatProgressBarModule } from '@angular/material/progress-bar';
import { MatBadgeModule } from '@angular/material/badge';
import { MatDividerModule } from '@angular/material/divider';
import { MatTooltipModule } from '@angular/material/tooltip';
import { MatSnackBarModule, MatSnackBar } from '@angular/material/snack-bar';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { AuthService } from '../../core/auth/auth.service';
import { DashboardService, DashboardMatch, DashboardBet, DashboardStats, DashboardLeague } from '../../core/services/dashboard.service';
import { Subscription } from 'rxjs';

// Use interfaces from dashboard service
interface League extends DashboardLeague {}
interface Match extends DashboardMatch {}
interface UserStats extends DashboardStats {}
interface Bet extends DashboardBet {}

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [
    CommonModule, 
    MatCardModule, 
    MatButtonModule, 
    MatIconModule,
    MatTabsModule,
    MatChipsModule,
    MatProgressBarModule,
    MatBadgeModule,
    MatDividerModule,
    MatTooltipModule,
    MatSnackBarModule,
    MatProgressSpinnerModule
  ],
  template: `
    <div class="dashboard-container">
      <!-- Loading spinner -->
      <div *ngIf="isLoading" class="loading-container">
        <mat-spinner></mat-spinner>
        <p>Loading your betting dashboard...</p>
      </div>

      <!-- Dashboard content -->
      <div *ngIf="!isLoading">
        <!-- Welcome Header -->
        <mat-card class="welcome-card">
          <mat-card-header>
            <mat-card-title>
              <mat-icon>sports</mat-icon>
              Welcome back, {{ currentUser?.firstName || currentUser?.username || 'Champion' }}!
            </mat-card-title>
            <mat-card-subtitle>Your betting dashboard • {{ getCurrentTime() }}</mat-card-subtitle>
          </mat-card-header>
          <mat-card-content>
            <div class="welcome-stats">
              <div class="stat-item">
                <span class="stat-value">{{ userStats.activeBets }}</span>
                <span class="stat-label">Active Bets</span>
              </div>
              <div class="stat-item">
                <span class="stat-value">{{ userStats.winRate | number:'1.0-1' }}%</span>
                <span class="stat-label">Win Rate</span>
              </div>
              <div class="stat-item">
                <span class="stat-value">{{ userStats.profit | currency:'EUR':'symbol':'1.0-0' }}</span>
                <span class="stat-label">Net Profit</span>
              </div>
            </div>
          </mat-card-content>
        </mat-card>

        <!-- Main Content Tabs -->
        <mat-card class="main-content-card">
          <mat-tab-group>
            <!-- Live Matches Tab -->
            <mat-tab>
              <ng-template mat-tab-label>
                <mat-icon>live_tv</mat-icon>
                Live Matches
                <mat-chip *ngIf="liveMatches.length > 0" [matBadge]="liveMatches.length" matBadgePosition="after">
                  {{ liveMatches.length }}
                </mat-chip>
              </ng-template>
              
              <div class="tab-content">
                <div *ngIf="liveMatches.length === 0" class="no-data">
                  <mat-icon>sports</mat-icon>
                  <h3>No live matches at the moment</h3>
                  <p>Check back later or browse upcoming matches</p>
                </div>
                
                <div *ngIf="liveMatches.length > 0" class="matches-grid">
                  <mat-card *ngFor="let match of liveMatches" class="match-card live-match">
                    <mat-card-header>
                      <div class="match-header">
                        <span class="league-name">{{ getLeagueName(match.leagueId) }}</span>
                        <mat-chip color="accent">
                          <mat-icon>live_tv</mat-icon>
                          LIVE {{ match.liveData?.minute }}'
                        </mat-chip>
                      </div>
                    </mat-card-header>
                    
                    <mat-card-content>
                      <div class="match-info">
                        <div class="team">
                          <img [src]="match.homeTeamLogo" alt="{{ match.homeTeam }}" class="team-logo" />
                          <span class="team-name">{{ match.homeTeam }}</span>
                        </div>
                        <div class="score-section">
                          <span class="score">{{ match.homeScore || 0 }}</span>
                          <span class="vs-divider">-</span>
                          <span class="score">{{ match.awayScore || 0 }}</span>
                        </div>
                        <div class="team">
                          <span class="team-name">{{ match.awayTeam }}</span>
                          <img [src]="match.awayTeamLogo" alt="{{ match.awayTeam }}" class="team-logo" />
                        </div>
                      </div>
                      
                      <div *ngIf="match.liveData" class="live-stats">
                        <div class="possession">
                          <span>{{ match.liveData.possession.home }}%</span>
                          <div class="possession-bar">
                            <div class="possession-home" [style.width.%]="match.liveData.possession.home"></div>
                            <div class="possession-away" [style.width.%]="match.liveData.possession.away"></div>
                          </div>
                          <span>{{ match.liveData.possession.away }}%</span>
                        </div>
                      </div>
                      
                      <div class="betting-odds">
                        <button mat-stroked-button class="odds-button" (click)="placeBet(match, 'home')">
                          <span class="odds-label">{{ match.homeTeam }}</span>
                          <span class="odds-value">{{ match.odds.home }}</span>
                        </button>
                        <button mat-stroked-button class="odds-button" (click)="placeBet(match, 'draw')">
                          <span class="odds-label">Draw</span>
                          <span class="odds-value">{{ match.odds.draw }}</span>
                        </button>
                        <button mat-stroked-button class="odds-button" (click)="placeBet(match, 'away')">
                          <span class="odds-label">{{ match.awayTeam }}</span>
                          <span class="odds-value">{{ match.odds.away }}</span>
                        </button>
                      </div>
                    </mat-card-content>
                  </mat-card>
                </div>
              </div>
            </mat-tab>

            <!-- Upcoming Matches Tab -->
            <mat-tab>
              <ng-template mat-tab-label>
                <mat-icon>schedule</mat-icon>
                Upcoming
                <mat-chip *ngIf="upcomingMatches.length > 0" [matBadge]="upcomingMatches.length" matBadgePosition="after">
                  {{ upcomingMatches.length }}
                </mat-chip>
              </ng-template>
              
              <div class="tab-content">
                <div *ngIf="upcomingMatches.length === 0" class="no-data">
                  <mat-icon>schedule</mat-icon>
                  <h3>No upcoming matches</h3>
                  <p>New matches will appear here when scheduled</p>
                </div>
                
                <div *ngIf="upcomingMatches.length > 0" class="matches-grid">
                  <mat-card *ngFor="let match of upcomingMatches" class="match-card">
                    <mat-card-header>
                      <div class="match-header">
                        <span class="league-name">{{ getLeagueName(match.leagueId) }}</span>
                        <span class="kickoff-time">{{ match.kickoff | date:'short' }}</span>
                      </div>
                    </mat-card-header>
                    
                    <mat-card-content>
                      <div class="match-info">
                        <div class="team">
                          <img [src]="match.homeTeamLogo" alt="{{ match.homeTeam }}" class="team-logo" />
                          <span class="team-name">{{ match.homeTeam }}</span>
                        </div>
                        <div class="vs-divider">vs</div>
                        <div class="team">
                          <span class="team-name">{{ match.awayTeam }}</span>
                          <img [src]="match.awayTeamLogo" alt="{{ match.awayTeam }}" class="team-logo" />
                        </div>
                      </div>
                      
                      <div class="betting-odds">
                        <button mat-stroked-button class="odds-button" (click)="placeBet(match, 'home')">
                          <span class="odds-label">{{ match.homeTeam }}</span>
                          <span class="odds-value">{{ match.odds.home }}</span>
                        </button>
                        <button mat-stroked-button class="odds-button" (click)="placeBet(match, 'draw')">
                          <span class="odds-label">Draw</span>
                          <span class="odds-value">{{ match.odds.draw }}</span>
                        </button>
                        <button mat-stroked-button class="odds-button" (click)="placeBet(match, 'away')">
                          <span class="odds-label">{{ match.awayTeam }}</span>
                          <span class="odds-value">{{ match.odds.away }}</span>
                        </button>
                      </div>
                    </mat-card-content>
                  </mat-card>
                </div>
              </div>
            </mat-tab>

            <!-- My Bets Tab -->
            <mat-tab>
              <ng-template mat-tab-label>
                <mat-icon>receipt</mat-icon>
                My Bets
                <mat-chip *ngIf="userBets.length > 0" [matBadge]="userBets.length" matBadgePosition="after">
                  {{ userBets.length }}
                </mat-chip>
              </ng-template>
              
              <div class="tab-content">
                <div *ngIf="userBets.length === 0" class="no-data">
                  <mat-icon>receipt</mat-icon>
                  <h3>No bets placed yet</h3>
                  <p>Start betting on your favorite matches!</p>
                  <button mat-raised-button color="primary" (click)="navigateToMatches()">
                    <mat-icon>sports</mat-icon>
                    Browse Matches
                  </button>
                </div>
                
                <div *ngIf="userBets.length > 0" class="bets-list">
                  <mat-card *ngFor="let bet of userBets" class="bet-card" [ngClass]="'bet-' + bet.status">
                    <mat-card-header>
                      <div class="bet-header">
                        <span class="bet-match">{{ bet.match }}</span>
                        <mat-chip [color]="getBetStatusColor(bet.status)">
                          <mat-icon>{{ getBetStatusIcon(bet.status) }}</mat-icon>
                          {{ bet.status | titlecase }}
                        </mat-chip>
                      </div>
                    </mat-card-header>
                    
                    <mat-card-content>
                      <div class="bet-details">
                        <div class="bet-info">
                          <div class="bet-prediction">{{ bet.prediction }}</div>
                          <div class="bet-odds">Odds: {{ bet.odds }}</div>
                        </div>
                        <div class="bet-amounts">
                          <div class="bet-stake">Stake: {{ bet.stake | currency:'EUR':'symbol':'1.0-0' }}</div>
                          <div class="bet-potential">Potential: {{ bet.potentialWin | currency:'EUR':'symbol':'1.0-0' }}</div>
                        </div>
                      </div>
                      <div class="bet-date">{{ bet.placedAt | date:'medium' }}</div>
                    </mat-card-content>
                  </mat-card>
                </div>
              </div>
            </mat-tab>

            <!-- Leagues Tab -->
            <mat-tab>
              <ng-template mat-tab-label>
                <mat-icon>emoji_events</mat-icon>
                Leagues
                <mat-chip *ngIf="leagues.length > 0" [matBadge]="leagues.length" matBadgePosition="after">
                  {{ leagues.length }}
                </mat-chip>
              </ng-template>
              
              <div class="tab-content">
                <div *ngIf="leagues.length === 0" class="no-data">
                  <mat-icon>emoji_events</mat-icon>
                  <h3>No leagues available</h3>
                  <p>Leagues will appear here when competitions are scheduled</p>
                </div>
                
                <div *ngIf="leagues.length > 0" class="leagues-grid">
                  <mat-card *ngFor="let league of leagues" class="league-card" (click)="viewLeague(league)">
                    <mat-card-header>
                      <mat-card-title>
                        <mat-icon>{{ league.icon }}</mat-icon>
                        {{ league.name }}
                      </mat-card-title>
                      <mat-card-subtitle>{{ league.country }} • {{ league.season }}</mat-card-subtitle>
                    </mat-card-header>
                    
                    <mat-card-content>
                      <div class="league-stats">
                        <div class="match-count">{{ league.matchCount }} matches</div>
                      </div>
                    </mat-card-content>
                    
                    <mat-card-actions>
                      <button mat-button color="primary">
                        <mat-icon>sports</mat-icon>
                        View Matches
                      </button>
                    </mat-card-actions>
                  </mat-card>
                </div>
              </div>
            </mat-tab>
          </mat-tab-group>
        </mat-card>

        <!-- Statistics and Ranking -->
        <div class="stats-grid">
          <mat-card class="stats-card">
            <mat-card-header>
              <mat-card-title>Betting Statistics</mat-card-title>
            </mat-card-header>
            <mat-card-content>
              <div class="stat-row">
                <span class="stat-label">Total Bets</span>
                <span class="stat-value">{{ userStats.totalBets }}</span>
              </div>
              <mat-divider></mat-divider>
              <div class="stat-row">
                <span class="stat-label">Active Bets</span>
                <span class="stat-value">{{ userStats.activeBets }}</span>
              </div>
              <mat-divider></mat-divider>
              <div class="stat-row">
                <span class="stat-label">Won</span>
                <span class="stat-value success">{{ userStats.wins }}</span>
              </div>
              <mat-divider></mat-divider>
              <div class="stat-row">
                <span class="stat-label">Lost</span>
                <span class="stat-value error">{{ userStats.losses }}</span>
              </div>
              <mat-divider></mat-divider>
              <div class="stat-row">
                <span class="stat-label">Total Stake</span>
                <span class="stat-value">{{ userStats.totalStake | currency:'EUR':'symbol':'1.0-0' }}</span>
              </div>
              <mat-divider></mat-divider>
              <div class="stat-row">
                <span class="stat-label">Total Winnings</span>
                <span class="stat-value">{{ userStats.totalWinnings | currency:'EUR':'symbol':'1.0-0' }}</span>
              </div>
              <mat-divider></mat-divider>
              <div class="stat-row highlight">
                <span class="stat-label">Net Profit</span>
                <span class="stat-value" [ngClass]="userStats.profit >= 0 ? 'success' : 'error'">
                  {{ userStats.profit >= 0 ? '+' : '' }}{{ userStats.profit | currency:'EUR':'symbol':'1.0-0' }}
                </span>
              </div>
            </mat-card-content>
          </mat-card>

          <mat-card class="ranking-card">
            <mat-card-header>
              <mat-card-title>Championship Ranking</mat-card-title>
            </mat-card-header>
            <mat-card-content>
              <div class="rank-display">
                <div class="current-rank">
                  <span class="rank-number">#{{ userStats.currentRank }}</span>
                  <span class="rank-label">Your Position</span>
                </div>
                <div class="rank-context">
                  <span>out of {{ userStats.totalUsers }} players</span>
                </div>
              </div>
              <mat-progress-bar 
                mode="determinate" 
                [value]="getRankProgressValue()" 
                color="accent">
              </mat-progress-bar>
              <div class="rank-actions">
                <button mat-raised-button color="primary">
                  <mat-icon>leaderboard</mat-icon>
                  View Full Leaderboard
                </button>
              </div>
            </mat-card-content>
          </mat-card>
        </div>
      </div>
    </div>
  `,
  styles: [`
    .dashboard-container {
      padding: 20px;
      max-width: 1400px;
      margin: 0 auto;
      background: #f5f5f5;
      min-height: 100vh;
    }

    .loading-container {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      min-height: 400px;
      gap: 20px;
    }

    .no-data {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      padding: 60px 20px;
      text-align: center;
      color: #666;
    }

    .no-data mat-icon {
      font-size: 64px;
      width: 64px;
      height: 64px;
      margin-bottom: 16px;
      opacity: 0.5;
    }

    .welcome-card {
      margin-bottom: 24px;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white;
    }

    .welcome-card mat-card-title {
      display: flex;
      align-items: center;
      gap: 8px;
      font-size: 1.5rem;
    }

    .welcome-stats {
      display: flex;
      justify-content: space-around;
      margin-top: 16px;
    }

    .stat-item {
      text-align: center;
    }

    .stat-value {
      display: block;
      font-size: 1.8rem;
      font-weight: bold;
      color: #fff;
    }

    .stat-label {
      display: block;
      font-size: 0.9rem;
      opacity: 0.9;
    }

    .main-content-card {
      margin-bottom: 24px;
    }

    .tab-content {
      padding: 20px;
      min-height: 400px;
    }

    .matches-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
      gap: 16px;
    }

    .match-card {
      transition: transform 0.2s ease, box-shadow 0.2s ease;
    }

    .match-card:hover {
      transform: translateY(-2px);
      box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }

    .live-match {
      border-left: 4px solid #ff5722;
    }

    .match-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      width: 100%;
    }

    .league-name {
      font-size: 0.9rem;
      color: #666;
    }

    .kickoff-time {
      font-weight: 500;
      color: #333;
    }

    .match-info {
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin: 16px 0;
    }

    .team {
      display: flex;
      align-items: center;
      gap: 8px;
      flex: 1;
    }

    .team:last-child {
      flex-direction: row-reverse;
    }

    .team-logo {
      width: 32px;
      height: 32px;
      border-radius: 50%;
      object-fit: cover;
    }

    .team-name {
      font-weight: 500;
      font-size: 0.95rem;
    }

    .score-section {
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .score {
      font-size: 1.5rem;
      font-weight: bold;
      color: #333;
      min-width: 24px;
      text-align: center;
    }

    .vs-divider {
      font-size: 0.8rem;
      color: #999;
      font-weight: 500;
      margin: 0 16px;
    }

    .live-stats {
      margin-top: 16px;
      padding-top: 16px;
      border-top: 1px solid #eee;
    }

    .possession {
      display: flex;
      align-items: center;
      gap: 12px;
      font-size: 0.9rem;
    }

    .possession-bar {
      flex: 1;
      display: flex;
      height: 8px;
      border-radius: 4px;
      overflow: hidden;
    }

    .possession-home {
      background: #3f51b5;
    }

    .possession-away {
      background: #ff5722;
    }

    .betting-odds {
      display: flex;
      gap: 8px;
      margin-top: 16px;
    }

    .odds-button {
      flex: 1;
      display: flex;
      flex-direction: column;
      padding: 8px;
      min-height: 60px;
    }

    .odds-label {
      font-size: 0.8rem;
      margin-bottom: 4px;
    }

    .odds-value {
      font-size: 1.1rem;
      font-weight: bold;
      color: #2196f3;
    }

    .bets-list {
      display: flex;
      flex-direction: column;
      gap: 16px;
    }

    .bet-card {
      transition: border-left 0.3s ease;
    }

    .bet-card.bet-pending {
      border-left: 4px solid #ff9800;
    }

    .bet-card.bet-won {
      border-left: 4px solid #4caf50;
    }

    .bet-card.bet-lost {
      border-left: 4px solid #f44336;
    }

    .bet-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 12px;
    }

    .bet-match {
      font-weight: 500;
      font-size: 1rem;
    }

    .bet-details {
      display: flex;
      justify-content: space-between;
      margin-bottom: 8px;
    }

    .bet-info, .bet-amounts {
      display: flex;
      flex-direction: column;
      gap: 4px;
    }

    .bet-prediction {
      font-weight: 500;
      color: #333;
    }

    .bet-odds {
      color: #666;
      font-size: 0.9rem;
    }

    .bet-stake, .bet-potential {
      font-size: 0.9rem;
      color: #666;
    }

    .bet-date {
      font-size: 0.8rem;
      color: #999;
    }

    .leagues-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
      gap: 16px;
    }

    .league-card {
      cursor: pointer;
      transition: transform 0.2s ease, box-shadow 0.2s ease;
    }

    .league-card:hover {
      transform: translateY(-2px);
      box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }

    .league-stats {
      margin: 12px 0;
    }

    .match-count {
      font-size: 0.9rem;
      color: #666;
    }

    .stats-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
      gap: 24px;
    }

    .stats-card, .ranking-card {
      background: white;
    }

    .stat-row {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 8px 0;
    }

    .stat-row.highlight {
      font-weight: 500;
      font-size: 1.1rem;
      padding: 12px 0;
    }

    .stat-label {
      color: #666;
    }

    .stat-value.success {
      color: #4caf50;
    }

    .stat-value.error {
      color: #f44336;
    }

    .rank-display {
      text-align: center;
      margin-bottom: 16px;
    }

    .current-rank {
      display: flex;
      flex-direction: column;
      align-items: center;
      margin-bottom: 8px;
    }

    .rank-number {
      font-size: 2.5rem;
      font-weight: bold;
      color: #3f51b5;
    }

    .rank-label {
      font-size: 0.9rem;
      color: #666;
    }

    .rank-context {
      font-size: 0.9rem;
      color: #666;
      margin-bottom: 16px;
    }

    .rank-actions {
      margin-top: 16px;
      text-align: center;
    }

    mat-tab-group {
      background: white;
    }

    mat-chip mat-icon {
      margin-right: 4px !important;
      font-size: 16px;
    }

    .success {
      color: #4caf50 !important;
    }

    .error {
      color: #f44336 !important;
    }

    @media (max-width: 768px) {
      .dashboard-container {
        padding: 10px;
      }

      .welcome-stats {
        flex-direction: column;
        gap: 16px;
      }

      .matches-grid {
        grid-template-columns: 1fr;
      }

      .stats-grid {
        grid-template-columns: 1fr;
      }

      .match-info {
        flex-direction: column;
        gap: 12px;
      }

      .team {
        justify-content: center;
      }

      .team:last-child {
        flex-direction: row;
      }
    }
  `]
})
export class DashboardComponent implements OnInit, OnDestroy {
  currentUser: any = null;
  isLoading = true;
  
  // Data arrays - will be populated from API
  leagues: League[] = [];
  liveMatches: Match[] = [];
  upcomingMatches: Match[] = [];
  userBets: Bet[] = [];
  userStats: UserStats = {
    totalBets: 0,
    activeBets: 0,
    wins: 0,
    losses: 0,
    winRate: 0,
    totalStake: 0,
    totalWinnings: 0,
    profit: 0,
    currentRank: 0,
    totalUsers: 0
  };

  private subscriptions: Subscription[] = [];

  constructor(
    private authService: AuthService,
    private dashboardService: DashboardService,
    private snackBar: MatSnackBar
  ) {
    this.currentUser = this.authService.getCurrentUser();
  }

  ngOnInit(): void {
    // Subscribe to user changes
    this.authService.currentUser$.subscribe((user: any) => {
      this.currentUser = user;
      if (user) {
        this.loadDashboardData();
      }
    });

    // Subscribe to dashboard data streams
    this.subscribeToData();
    
    // Start live updates
    this.dashboardService.startLiveUpdates();
  }

  ngOnDestroy(): void {
    // Clean up subscriptions
    this.subscriptions.forEach(sub => sub.unsubscribe());
    this.dashboardService.stopLiveUpdates();
  }

  private subscribeToData(): void {
    // Subscribe to live matches
    this.subscriptions.push(
      this.dashboardService.getLiveMatches().subscribe({
        next: (matches) => {
          this.liveMatches = matches;
        },
        error: (error) => {
          console.error('Error loading live matches:', error);
          this.showError('Failed to load live matches');
        }
      })
    );

    // Subscribe to upcoming matches
    this.subscriptions.push(
      this.dashboardService.getUpcomingMatches().subscribe({
        next: (matches) => {
          this.upcomingMatches = matches;
        },
        error: (error) => {
          console.error('Error loading upcoming matches:', error);
          this.showError('Failed to load upcoming matches');
        }
      })
    );

    // Subscribe to user bets
    this.subscriptions.push(
      this.dashboardService.getUserBets().subscribe({
        next: (bets) => {
          this.userBets = bets;
        },
        error: (error) => {
          console.error('Error loading user bets:', error);
          this.showError('Failed to load your bets');
        }
      })
    );

    // Subscribe to user stats
    this.subscriptions.push(
      this.dashboardService.getUserStats().subscribe({
        next: (stats) => {
          this.userStats = stats;
        },
        error: (error) => {
          console.error('Error loading user stats:', error);
          this.showError('Failed to load statistics');
        }
      })
    );

    // Subscribe to leagues
    this.subscriptions.push(
      this.dashboardService.getLeagues().subscribe({
        next: (leagues) => {
          this.leagues = leagues;
        },
        error: (error) => {
          console.error('Error loading leagues:', error);
          this.showError('Failed to load leagues');
        }
      })
    );
  }

  private async loadDashboardData(): Promise<void> {
    this.isLoading = true;
    try {
      await this.dashboardService.loadDashboardData();
      this.isLoading = false;
    } catch (error) {
      console.error('Error loading dashboard data:', error);
      this.showError('Failed to load dashboard data');
      this.isLoading = false;
    }
  }

  private showError(message: string): void {
    this.snackBar.open(message, 'Close', {
      duration: 5000,
      horizontalPosition: 'end',
      verticalPosition: 'top'
    });
  }

  getCurrentTime(): string {
    return new Date().toLocaleDateString('en-US', {
      weekday: 'long',
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  }

  getLeagueName(leagueId: string): string {
    const league = this.leagues.find(l => l.id === leagueId);
    return league ? league.name : 'Unknown League';
  }

  getBetStatusColor(status: string): string {
    switch (status) {
      case 'pending': return 'warn';
      case 'won': return 'primary';
      case 'lost': return 'accent';
      default: return 'primary';
    }
  }

  getBetStatusIcon(status: string): string {
    switch (status) {
      case 'pending': return 'hourglass_empty';
      case 'won': return 'check_circle';
      case 'lost': return 'cancel';
      default: return 'help';
    }
  }

  getRankProgressValue(): number {
    if (this.userStats.totalUsers === 0) return 0;
    // Calculate progress from bottom to current rank
    return ((this.userStats.totalUsers - this.userStats.currentRank) / this.userStats.totalUsers) * 100;
  }

  async placeBet(match: Match, prediction: 'home' | 'draw' | 'away'): Promise<void> {
    try {
      const predictionText = prediction === 'home' ? match.homeTeam : 
                            prediction === 'away' ? match.awayTeam : 'Draw';
      
      // For now, show a simple prompt for stake amount
      const stakeInput = prompt(`Place bet on: ${predictionText} @ ${match.odds[prediction]}\n\nEnter stake amount (EUR):`);
      
      if (stakeInput && !isNaN(Number(stakeInput))) {
        const stake = Number(stakeInput);
        
        this.dashboardService.placeBet(match.id, prediction, match.odds[prediction], stake).subscribe({
          next: (bet) => {
            this.snackBar.open(`Bet placed successfully! Potential win: €${bet.potential_payout}`, 'Close', {
              duration: 5000,
              panelClass: ['success-snackbar']
            });
            // Refresh data to show new bet
            this.loadDashboardData();
          },
          error: (error) => {
            console.error('Error placing bet:', error);
            this.showError('Failed to place bet. Please try again.');
          }
        });
      }
    } catch (error) {
      console.error('Error in placeBet:', error);
      this.showError('An error occurred while placing the bet');
    }
  }

  viewLeague(league: League): void {
    // This would navigate to a league details page in a real app
    this.snackBar.open(`Viewing ${league.name} matches`, 'Close', {
      duration: 3000
    });
  }

  navigateToMatches(): void {
    // This would navigate to matches page in a real app
    this.snackBar.open('Navigate to matches page', 'Close', {
      duration: 3000
    });
  }
}