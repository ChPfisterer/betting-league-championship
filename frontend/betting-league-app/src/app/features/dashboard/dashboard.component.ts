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
import { AuthService } from '../../core/auth/auth.service';
import { DashboardService, DashboardMatch, DashboardBet, DashboardStats, DashboardLeague } from '../../core/services/dashboard.service';
import { Subscription } from 'rxjs';

// Use interfaces from dashboard service instead of local ones
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
    MatSnackBarModule
  ],
  template: `
    <div class="dashboard-container">
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
              <span class="stat-value">{{ userStats.profit >= 0 ? '+' : '' }}{{ userStats.profit | currency:'EUR':'symbol':'1.0-0' }}</span>
              <span class="stat-label">Total Profit</span>
            </div>
            <div class="stat-item">
              <span class="stat-value">#{{ userStats.currentRank }}</span>
              <span class="stat-label">Current Rank</span>
            </div>
          </div>
        </mat-card-content>
      </mat-card>

      <!-- Main Content Tabs -->
      <mat-card class="main-content-card">
        <mat-tab-group>
          <!-- Live Matches Tab -->
          <mat-tab label="Live Matches" [disabled]="false">
            <ng-template matTabContent>
              <div class="tab-content">
                <div class="matches-grid">
                  <mat-card *ngFor="let match of liveMatches" class="match-card live-match">
                    <mat-card-header>
                      <div class="match-header">
                        <mat-chip color="accent">
                          <mat-icon>radio_button_checked</mat-icon>
                          LIVE {{ match.liveData?.minute }}'
                        </mat-chip>
                        <span class="league-name">{{ getLeagueName(match.leagueId) }}</span>
                      </div>
                    </mat-card-header>
                    <mat-card-content>
                      <div class="match-info">
                        <div class="team">
                          <img [src]="match.homeTeamLogo" [alt]="match.homeTeam" class="team-logo">
                          <span class="team-name">{{ match.homeTeam }}</span>
                          <span class="score">{{ match.homeScore }}</span>
                        </div>
                        <div class="vs-divider">VS</div>
                        <div class="team">
                          <span class="score">{{ match.awayScore }}</span>
                          <span class="team-name">{{ match.awayTeam }}</span>
                          <img [src]="match.awayTeamLogo" [alt]="match.awayTeam" class="team-logo">
                        </div>
                      </div>
                      <div class="live-stats" *ngIf="match.liveData">
                        <div class="possession">
                          <span>Possession</span>
                          <div class="possession-bar">
                            <mat-progress-bar mode="determinate" [value]="match.liveData.possession.home" color="primary"></mat-progress-bar>
                            <mat-progress-bar mode="determinate" [value]="match.liveData.possession.away" color="accent"></mat-progress-bar>
                          </div>
                          <span>{{ match.liveData.possession.home }}% - {{ match.liveData.possession.away }}%</span>
                        </div>
                      </div>
                    </mat-card-content>
                  </mat-card>
                </div>
              </div>
            </ng-template>
          </mat-tab>

          <!-- Upcoming Matches Tab -->
          <mat-tab label="Upcoming Matches">
            <ng-template matTabContent>
              <div class="tab-content">
                <div class="matches-grid">
                  <mat-card *ngFor="let match of upcomingMatches" class="match-card">
                    <mat-card-header>
                      <div class="match-header">
                        <span class="kickoff-time">{{ match.kickoff | date:'short' }}</span>
                        <span class="league-name">{{ getLeagueName(match.leagueId) }}</span>
                      </div>
                    </mat-card-header>
                    <mat-card-content>
                      <div class="match-info">
                        <div class="team">
                          <img [src]="match.homeTeamLogo" [alt]="match.homeTeam" class="team-logo">
                          <span class="team-name">{{ match.homeTeam }}</span>
                        </div>
                        <div class="vs-divider">VS</div>
                        <div class="team">
                          <span class="team-name">{{ match.awayTeam }}</span>
                          <img [src]="match.awayTeamLogo" [alt]="match.awayTeam" class="team-logo">
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
            </ng-template>
          </mat-tab>

          <!-- My Bets Tab -->
          <mat-tab [label]="'My Bets (' + userBets.length + ')'">
            <ng-template matTabContent>
              <div class="tab-content">
                <div class="bets-list">
                  <mat-card *ngFor="let bet of userBets" class="bet-card" [ngClass]="'bet-' + bet.status">
                    <mat-card-content>
                      <div class="bet-header">
                        <span class="bet-match">{{ bet.match }}</span>
                        <mat-chip [color]="getBetStatusColor(bet.status)">
                          {{ bet.status | uppercase }}
                        </mat-chip>
                      </div>
                      <div class="bet-details">
                        <div class="bet-info">
                          <span class="bet-prediction">{{ bet.prediction }}</span>
                          <span class="bet-odds">@ {{ bet.odds }}</span>
                        </div>
                        <div class="bet-amounts">
                          <span class="bet-stake">Stake: {{ bet.stake | currency:'EUR':'symbol':'1.0-0' }}</span>
                          <span class="bet-potential">Potential: {{ bet.potentialWin | currency:'EUR':'symbol':'1.0-0' }}</span>
                        </div>
                      </div>
                      <div class="bet-footer">
                        <span class="bet-date">{{ bet.placedAt | date:'short' }}</span>
                      </div>
                    </mat-card-content>
                  </mat-card>
                </div>
              </div>
            </ng-template>
          </mat-tab>

          <!-- Leagues Tab -->
          <mat-tab label="Leagues">
            <ng-template matTabContent>
              <div class="tab-content">
                <div class="leagues-grid">
                  <mat-card *ngFor="let league of leagues" class="league-card" (click)="viewLeague(league)">
                    <mat-card-header>
                      <div mat-card-avatar>
                        <mat-icon>{{ league.icon }}</mat-icon>
                      </div>
                      <mat-card-title>{{ league.name }}</mat-card-title>
                      <mat-card-subtitle>{{ league.country }} • {{ league.season }}</mat-card-subtitle>
                    </mat-card-header>
                    <mat-card-content>
                      <div class="league-stats">
                        <span class="match-count">{{ league.matchCount }} matches available</span>
                      </div>
                    </mat-card-content>
                    <mat-card-actions>
                      <button mat-button color="primary">View Matches</button>
                    </mat-card-actions>
                  </mat-card>
                </div>
              </div>
            </ng-template>
          </mat-tab>
        </mat-tab-group>
      </mat-card>

      <!-- Stats Summary -->
      <div class="stats-grid">
        <mat-card class="stats-card">
          <mat-card-header>
            <mat-card-title>Performance Stats</mat-card-title>
          </mat-card-header>
          <mat-card-content>
            <div class="stat-row">
              <span class="stat-label">Total Bets</span>
              <span class="stat-value">{{ userStats.totalBets }}</span>
            </div>
            <div class="stat-row">
              <span class="stat-label">Wins</span>
              <span class="stat-value success">{{ userStats.wins }}</span>
            </div>
            <div class="stat-row">
              <span class="stat-label">Losses</span>
              <span class="stat-value error">{{ userStats.losses }}</span>
            </div>
            <div class="stat-row">
              <span class="stat-label">Win Rate</span>
              <span class="stat-value">{{ userStats.winRate }}%</span>
            </div>
            <mat-divider></mat-divider>
            <div class="stat-row">
              <span class="stat-label">Total Stake</span>
              <span class="stat-value">{{ userStats.totalStake | currency:'EUR':'symbol':'1.0-0' }}</span>
            </div>
            <div class="stat-row">
              <span class="stat-label">Total Winnings</span>
              <span class="stat-value">{{ userStats.totalWinnings | currency:'EUR':'symbol':'1.0-0' }}</span>
            </div>
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
  `,
  styles: [`
    .dashboard-container {
      padding: 20px;
      max-width: 1400px;
      margin: 0 auto;
      background: #f5f5f5;
      min-height: 100vh;
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
        padding: 12px;
      }

      .matches-grid, .leagues-grid {
        grid-template-columns: 1fr;
      }

      .welcome-stats {
        flex-direction: column;
        gap: 16px;
      }

      .match-info {
        flex-direction: column;
        gap: 12px;
      }

      .betting-odds {
        flex-direction: column;
      }

      .bet-details {
        flex-direction: column;
        gap: 8px;
      }
    }
  `]
})
export class DashboardComponent implements OnInit {
  currentUser: any = null;
  
  // Mock data - In a real app, this would come from services
  leagues: League[] = [
    {
      id: '1',
      name: 'Premier League',
      sport: 'Football',
      country: 'England',
      icon: 'sports_soccer',
      season: '2024-25',
      matchCount: 15
    },
    {
      id: '2',
      name: 'La Liga',
      sport: 'Football',
      country: 'Spain',
      icon: 'sports_soccer',
      season: '2024-25',
      matchCount: 12
    },
    {
      id: '3',
      name: 'Bundesliga',
      sport: 'Football',
      country: 'Germany',
      icon: 'sports_soccer',
      season: '2024-25',
      matchCount: 10
    },
    {
      id: '4',
      name: 'NBA',
      sport: 'Basketball',
      country: 'USA',
      icon: 'sports_basketball',
      season: '2024-25',
      matchCount: 25
    }
  ];

  liveMatches: Match[] = [
    {
      id: '1',
      leagueId: '1',
      homeTeam: 'Manchester United',
      awayTeam: 'Liverpool',
      homeTeamLogo: 'https://logoeps.com/wp-content/uploads/2013/03/manchester-united-vector-logo.png',
      awayTeamLogo: 'https://logoeps.com/wp-content/uploads/2014/09/liverpool-vector-logo.png',
      kickoff: new Date(),
      status: 'live',
      homeScore: 1,
      awayScore: 2,
      odds: { home: 2.1, draw: 3.2, away: 3.8 },
      liveData: {
        minute: 67,
        possession: { home: 45, away: 55 }
      }
    },
    {
      id: '2',
      leagueId: '2',
      homeTeam: 'Real Madrid',
      awayTeam: 'Barcelona',
      homeTeamLogo: 'https://logoeps.com/wp-content/uploads/2013/03/real-madrid-vector-logo.png',
      awayTeamLogo: 'https://logoeps.com/wp-content/uploads/2013/03/barcelona-vector-logo.png',
      kickoff: new Date(),
      status: 'live',
      homeScore: 0,
      awayScore: 1,
      odds: { home: 1.9, draw: 3.4, away: 4.2 },
      liveData: {
        minute: 34,
        possession: { home: 62, away: 38 }
      }
    }
  ];

  upcomingMatches: Match[] = [
    {
      id: '3',
      leagueId: '1',
      homeTeam: 'Arsenal',
      awayTeam: 'Chelsea',
      homeTeamLogo: 'https://logoeps.com/wp-content/uploads/2013/03/arsenal-vector-logo.png',
      awayTeamLogo: 'https://logoeps.com/wp-content/uploads/2013/03/chelsea-vector-logo.png',
      kickoff: new Date(Date.now() + 2 * 60 * 60 * 1000), // 2 hours from now
      status: 'upcoming',
      odds: { home: 2.3, draw: 3.1, away: 2.9 }
    },
    {
      id: '4',
      leagueId: '3',
      homeTeam: 'Bayern Munich',
      awayTeam: 'Borussia Dortmund',
      homeTeamLogo: 'https://logoeps.com/wp-content/uploads/2013/03/bayern-munich-vector-logo.png',
      awayTeamLogo: 'https://logoeps.com/wp-content/uploads/2013/03/borussia-dortmund-vector-logo.png',
      kickoff: new Date(Date.now() + 4 * 60 * 60 * 1000), // 4 hours from now
      status: 'upcoming',
      odds: { home: 1.7, draw: 3.8, away: 4.5 }
    },
    {
      id: '5',
      leagueId: '4',
      homeTeam: 'Lakers',
      awayTeam: 'Warriors',
      homeTeamLogo: 'https://logoeps.com/wp-content/uploads/2014/09/los-angeles-lakers-vector-logo.png',
      awayTeamLogo: 'https://logoeps.com/wp-content/uploads/2014/09/golden-state-warriors-vector-logo.png',
      kickoff: new Date(Date.now() + 6 * 60 * 60 * 1000), // 6 hours from now
      status: 'upcoming',
      odds: { home: 1.9, draw: 21.0, away: 2.1 }
    }
  ];

  userBets: Bet[] = [
    {
      id: '1',
      matchId: '1',
      match: 'Manchester United vs Liverpool',
      prediction: 'Liverpool Win',
      odds: 3.8,
      stake: 25,
      potentialWin: 95,
      status: 'pending',
      placedAt: new Date(Date.now() - 30 * 60 * 1000) // 30 minutes ago
    },
    {
      id: '2',
      matchId: '3',
      match: 'Arsenal vs Chelsea',
      prediction: 'Draw',
      odds: 3.1,
      stake: 50,
      potentialWin: 155,
      status: 'pending',
      placedAt: new Date(Date.now() - 2 * 60 * 60 * 1000) // 2 hours ago
    },
    {
      id: '3',
      matchId: 'finished-1',
      match: 'AC Milan vs Inter Milan',
      prediction: 'AC Milan Win',
      odds: 2.4,
      stake: 30,
      potentialWin: 72,
      status: 'won',
      placedAt: new Date(Date.now() - 24 * 60 * 60 * 1000) // 1 day ago
    }
  ];

  userStats: UserStats = {
    totalBets: 15,
    activeBets: 2,
    wins: 8,
    losses: 5,
    winRate: 53.3,
    totalStake: 450,
    totalWinnings: 520,
    profit: 70,
    currentRank: 42,
    totalUsers: 1247
  };

  constructor(private authService: AuthService) {
    this.currentUser = this.authService.getCurrentUser();
  }

  ngOnInit(): void {
    // Subscribe to user changes
    this.authService.currentUser$.subscribe((user: any) => {
      this.currentUser = user;
    });

    // In a real app, you would load data here
    // this.loadDashboardData();
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

  getRankProgressValue(): number {
    // Calculate progress from bottom to current rank
    return ((this.userStats.totalUsers - this.userStats.currentRank) / this.userStats.totalUsers) * 100;
  }

  placeBet(match: Match, prediction: 'home' | 'draw' | 'away'): void {
    console.log(`Placing bet on ${match.homeTeam} vs ${match.awayTeam} - ${prediction}`);
    // In a real app, this would open a betting dialog
    // For now, just show a console message
    const predictionText = prediction === 'home' ? match.homeTeam : 
                          prediction === 'away' ? match.awayTeam : 'Draw';
    alert(`Betting on: ${predictionText} @ ${match.odds[prediction]}\n\nThis would open the betting slip in a real application.`);
  }

  viewLeague(league: League): void {
    console.log(`Viewing league: ${league.name}`);
    // In a real app, this would navigate to the league page
    alert(`Viewing ${league.name} matches\n\nThis would navigate to the league page in a real application.`);
  }
}