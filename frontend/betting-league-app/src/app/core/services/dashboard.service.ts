import { Injectable } from '@angular/core';
import { Observable, combineLatest, map, startWith } from 'rxjs';
import { ApiService, Match, Bet, Competition, Team } from './api.service';
import { AuthService } from '../auth/auth.service';

// Dashboard-specific interfaces that match our component
export interface DashboardMatch {
  id: string;
  leagueId: string;
  homeTeam: string;
  awayTeam: string;
  homeTeamLogo: string;
  awayTeamLogo: string;
  kickoff: Date;
  status: 'upcoming' | 'live' | 'finished';
  stage?: string; // e.g., "Group Stage", "Round of 16", "Quarter-final", "Semi-final", "Final"
  match_type?: string; // Original match type from API
  homeScore?: number;
  awayScore?: number;
  odds: {
    home: number;
    draw: number;
    away: number;
  };
  liveData?: {
    minute: number;
    possession: { home: number; away: number };
  };
}

export interface DashboardBet {
  id: string;
  matchId: string;
  match: string;
  prediction: string;
  odds: number;
  stake: number;
  potentialWin: number;
  status: 'pending' | 'won' | 'lost';
  placedAt: Date;
}

export interface DashboardStats {
  totalBets: number;
  activeBets: number;
  wins: number;
  losses: number;
  winRate: number;
  totalStake: number;
  totalWinnings: number;
  profit: number;
  currentRank: number;
  totalUsers: number;
}

export interface DashboardLeague {
  id: string;
  name: string;
  sport: string;
  country: string;
  icon: string;
  season: string;
  matchCount: number;
}

@Injectable({
  providedIn: 'root'
})
export class DashboardService {
  
  constructor(
    private apiService: ApiService,
    private authService: AuthService
  ) {}

  /**
   * Get live matches formatted for dashboard
   */
  getLiveMatches(): Observable<DashboardMatch[]> {
    return this.apiService.getMatchesByStatus('live').pipe(
      map(matches => {
        const dashboardMatches = matches.map(this.transformMatchToDashboard.bind(this));
        
        // If no live matches from API, generate some demo live matches for betting
        if (dashboardMatches.length === 0) {
          console.log('No live matches from API, generating demo live matches for betting');
          return this.generateLiveMatches();
        }
        
        return dashboardMatches;
      })
    );
  }

  /**
   * Get upcoming matches formatted for dashboard
   */
  getUpcomingMatches(): Observable<DashboardMatch[]> {
    return this.apiService.getMatchesByStatus('scheduled').pipe(
      map(matches => {
        const dashboardMatches = matches.map(this.transformMatchToDashboard.bind(this));
        
        // If no upcoming matches from API, generate some demo upcoming matches for betting
        if (dashboardMatches.length === 0) {
          console.log('No upcoming matches from API, generating demo upcoming matches for betting');
          return this.generateUpcomingMatches();
        }
        
        return dashboardMatches;
      })
    );
  }

  /**
   * Get recent finished matches formatted for dashboard
   */
  getRecentMatches(): Observable<DashboardMatch[]> {
    return this.apiService.getMatchesByStatus('finished').pipe(
      map(matches => matches.map(this.transformMatchToDashboard.bind(this)))
    );
  }

  /**
   * Get user bets formatted for dashboard
   */
  getUserBets(): Observable<DashboardBet[]> {
    return this.apiService.userBets$.pipe(
      map(bets => bets.map(this.transformBetToDashboard.bind(this)))
    );
  }

  /**
   * Get user statistics formatted for dashboard
   */
  getUserStats(): Observable<DashboardStats> {
    const currentUser = this.authService.getCurrentUser();
    
    return combineLatest([
      this.apiService.userStats$.pipe(startWith(null)),
      // We'll add leaderboard data later, for now use mock ranking
    ]).pipe(
      map(([stats]) => {
        if (!stats) {
          // Return default stats if no data available
          return {
            totalBets: 0,
            activeBets: 0,
            wins: 0,
            losses: 0,
            winRate: 0,
            totalStake: 0,
            totalWinnings: 0,
            profit: 0,
            currentRank: 0,
            totalUsers: 1247 // This should come from a real API
          };
        }

        return {
          totalBets: stats.total_bets,
          activeBets: stats.active_bets,
          wins: stats.won_bets,
          losses: stats.lost_bets,
          winRate: stats.win_rate,
          totalStake: stats.total_stake,
          totalWinnings: stats.total_winnings,
          profit: stats.net_profit,
          currentRank: 42, // TODO: Get from leaderboard API
          totalUsers: 1247 // TODO: Get from users count API
        };
      })
    );
  }

  /**
   * Get leagues/competitions formatted for dashboard
   */
  getLeagues(): Observable<DashboardLeague[]> {
    return this.apiService.getCompetitions().pipe(
      map(competitions => {
        if (competitions.length === 0) {
          // Fallback data if API returns empty (using known FIFA World Cup data)
          return [{
            id: '72306d02-fe54-42ee-b5db-50c230a1e6ab',
            name: 'FIFA World Cup 2022',
            sport: 'Football',
            country: 'International',
            icon: 'sports_soccer',
            season: '2022',
            matchCount: 64
          }];
        }
        return competitions.map(this.transformCompetitionToLeague.bind(this));
      })
    );
  }

  /**
   * Load all dashboard data for a user
   */
  async loadDashboardData(): Promise<void> {
    const currentUser = this.authService.getCurrentUser();
    if (!currentUser?.id) {
      console.error('No current user found');
      return;
    }

    await this.apiService.loadDashboardData(currentUser.id);
  }

  /**
   * Place a prediction through the API
   */
  placeBet(matchId: string, prediction: 'home' | 'draw' | 'away', odds: number, confidence: number): Observable<any> {
    // Map frontend prediction to backend BetOutcome enum
    const outcomeMap = {
      'home': 'home_win',
      'draw': 'draw', 
      'away': 'away_win'
    };

    // Calculate potential payout (required by backend)
    const amount = confidence; // Use confidence as amount for now (0-10 range)
    const potentialPayout = amount * odds;

    const predictionData = {
      match_id: matchId,
      bet_type: 'match_winner', // Backend expects this enum value
      amount: amount,
      odds: odds,
      potential_payout: potentialPayout,
      outcome: outcomeMap[prediction] // Map to backend enum
    };

    return this.apiService.placeBet(predictionData);
  }

  /**
   * Transform API Match to Dashboard Match
   */
  private transformMatchToDashboard(match: Match): DashboardMatch {
    return {
      id: match.id,
      leagueId: match.competition_id,
      homeTeam: match.home_team?.name || 'Unknown Team',
      awayTeam: match.away_team?.name || 'Unknown Team',
      homeTeamLogo: match.home_team?.logo_url || this.getDefaultTeamLogo(match.home_team?.country),
      awayTeamLogo: match.away_team?.logo_url || this.getDefaultTeamLogo(match.away_team?.country),
      kickoff: new Date(match.scheduled_at || match.match_date || new Date()),
      status: this.mapMatchStatus(match.status),
      stage: this.determineMatchStage(match),
      homeScore: match.home_score,
      awayScore: match.away_score,
      match_type: match.match_type,
      odds: this.generateOdds(match), // TODO: Get real odds from API
      liveData: match.status === 'live' ? this.generateLiveData() : undefined
    };
  }

  /**
   * Transform API Bet to Dashboard Bet
   */
  private transformBetToDashboard(bet: Bet): DashboardBet {
    const matchDisplay = bet.match ? 
      `${bet.match.home_team?.name || 'Team'} vs ${bet.match.away_team?.name || 'Team'}` : 
      'Unknown Match';

    return {
      id: bet.id,
      matchId: bet.match_id,
      match: matchDisplay,
      prediction: this.formatPrediction(bet.predicted_outcome, bet.match),
      odds: bet.odds,
      stake: bet.stake_amount,
      potentialWin: bet.potential_payout,
      status: bet.status as 'pending' | 'won' | 'lost',
      placedAt: new Date(bet.placed_at)
    };
  }

  /**
   * Transform API Competition to Dashboard League
   */
  private transformCompetitionToLeague(competition: Competition): DashboardLeague {
    return {
      id: competition.id,
      name: competition.name,
      sport: competition.sport?.name || 'Football',
      country: this.extractCountryFromCompetition(competition),
      icon: this.getSportIcon(competition.sport?.name),
      season: competition.season?.name || competition.season?.year?.toString() || '2024',
      matchCount: 0 // TODO: Get actual match count from API
    };
  }

  /**
   * Determine match stage/phase based on round number and match type
   */
  private determineMatchStage(match: Match): string {
    const roundNumber = match.round_number || 1;
    const matchType = match.match_type || 'regular';
    
    // For World Cup and knockout tournaments
    if (matchType === 'final') {
      return 'Final';
    } else if (matchType === 'semifinal') {
      return 'Semi-final';
    } else if (matchType === 'quarterfinal') {
      return 'Quarter-final';
    } else if (matchType === 'playoff') {
      // Determine playoff stage based on round number
      switch (roundNumber) {
        case 2: return 'Round of 16';
        case 3: return 'Quarter-final';
        case 4: return 'Semi-final';
        case 5: return '3rd Place Play-off';
        case 6: return 'Final';
        default: return 'Playoff Round';
      }
    } else {
      // For regular matches, determine stage based on round patterns
      if (roundNumber === 1) {
        return 'Group Stage';
      } else if (roundNumber === 2 && matchType === 'regular') {
        return 'Round of 16';
      } else if (roundNumber === 3) {
        return 'Quarter-final';
      } else if (roundNumber === 4) {
        return 'Semi-final';
      } else if (roundNumber === 5) {
        return '3rd Place Play-off';
      } else if (roundNumber === 6) {
        return 'Final';
      } else {
        // For regular league games
        return `Matchday ${roundNumber}`;
      }
    }
  }

  /**
   * Map API match status to dashboard status
   */
  private mapMatchStatus(status: string): 'upcoming' | 'live' | 'finished' {
    switch (status) {
      case 'scheduled': return 'upcoming';
      case 'live': return 'live';
      case 'completed': return 'finished';
      case 'finished': return 'finished';
      default: return 'upcoming';
    }
  }

  /**
   * Generate odds for a match (placeholder until we have real odds API)
   */
  private generateOdds(match: Match): { home: number; draw: number; away: number } {
    // TODO: Get real odds from betting API
    // For now, generate realistic-looking odds
    const base = Math.random() * 0.5 + 1.5; // 1.5 to 2.0
    return {
      home: Number((base + Math.random() * 1).toFixed(2)),
      draw: Number((3.0 + Math.random() * 0.8).toFixed(2)),
      away: Number((base + Math.random() * 1.5).toFixed(2))
    };
  }

  /**
   * Generate live match data (placeholder until we have real live data)
   */
  private generateLiveData(): { minute: number; possession: { home: number; away: number } } {
    const minute = Math.floor(Math.random() * 90) + 1;
    const homePossession = Math.floor(Math.random() * 40) + 30; // 30-70%
    return {
      minute,
      possession: {
        home: homePossession,
        away: 100 - homePossession
      }
    };
  }

  /**
   * Get default team logo based on country
   */
  private getDefaultTeamLogo(country?: string): string {
    if (!country) return '/assets/images/default-team-logo.png';
    
    // FIFA World Cup team logos mapping
    const teamLogos: { [key: string]: string } = {
      'Qatar': 'https://img.fifa.com/images/fls/crest-580/qatar.png',
      'Ecuador': 'https://img.fifa.com/images/fls/crest-580/ecuador.png',
      'England': 'https://img.fifa.com/images/fls/crest-580/england.png',
      'Iran': 'https://img.fifa.com/images/fls/crest-580/iran.png',
      'USA': 'https://img.fifa.com/images/fls/crest-580/usa.png',
      'Wales': 'https://img.fifa.com/images/fls/crest-580/wales.png',
      'Argentina': 'https://img.fifa.com/images/fls/crest-580/argentina.png',
      'Saudi Arabia': 'https://img.fifa.com/images/fls/crest-580/saudi-arabia.png',
      'Mexico': 'https://img.fifa.com/images/fls/crest-580/mexico.png',
      'Poland': 'https://img.fifa.com/images/fls/crest-580/poland.png',
      'France': 'https://img.fifa.com/images/fls/crest-580/france.png',
      'Australia': 'https://img.fifa.com/images/fls/crest-580/australia.png',
      'Denmark': 'https://img.fifa.com/images/fls/crest-580/denmark.png',
      'Tunisia': 'https://img.fifa.com/images/fls/crest-580/tunisia.png',
      'Spain': 'https://img.fifa.com/images/fls/crest-580/spain.png',
      'Costa Rica': 'https://img.fifa.com/images/fls/crest-580/costa-rica.png',
      'Germany': 'https://img.fifa.com/images/fls/crest-580/germany.png',
      'Japan': 'https://img.fifa.com/images/fls/crest-580/japan.png',
      'Belgium': 'https://img.fifa.com/images/fls/crest-580/belgium.png',
      'Canada': 'https://img.fifa.com/images/fls/crest-580/canada.png',
      'Morocco': 'https://img.fifa.com/images/fls/crest-580/morocco.png',
      'Croatia': 'https://img.fifa.com/images/fls/crest-580/croatia.png',
      'Brazil': 'https://img.fifa.com/images/fls/crest-580/brazil.png',
      'Serbia': 'https://img.fifa.com/images/fls/crest-580/serbia.png',
      'Switzerland': 'https://img.fifa.com/images/fls/crest-580/switzerland.png',
      'Cameroon': 'https://img.fifa.com/images/fls/crest-580/cameroon.png',
      'Portugal': 'https://img.fifa.com/images/fls/crest-580/portugal.png',
      'Ghana': 'https://img.fifa.com/images/fls/crest-580/ghana.png',
      'Uruguay': 'https://img.fifa.com/images/fls/crest-580/uruguay.png',
      'South Korea': 'https://img.fifa.com/images/fls/crest-580/south-korea.png',
      'Netherlands': 'https://img.fifa.com/images/fls/crest-580/netherlands.png',
      'Senegal': 'https://img.fifa.com/images/fls/crest-580/senegal.png'
    };
    
    return teamLogos[country] || '/assets/images/default-team-logo.png';
  }

  /**
   * Extract country from competition (for FIFA World Cup it's international)
   */
  private extractCountryFromCompetition(competition: Competition): string {
    if (competition.name.toLowerCase().includes('world cup')) {
      return 'International';
    }
    return 'Unknown';
  }

  /**
   * Get sport icon based on sport name
   */
  private getSportIcon(sportName?: string): string {
    switch (sportName?.toLowerCase()) {
      case 'football':
      case 'soccer':
        return 'sports_soccer';
      case 'basketball':
        return 'sports_basketball';
      case 'tennis':
        return 'sports_tennis';
      case 'hockey':
        return 'sports_hockey';
      default:
        return 'sports';
    }
  }

  /**
   * Format bet prediction for display
   */
  private formatPrediction(prediction: string, match?: Match): string {
    if (!match) return prediction;
    
    switch (prediction.toLowerCase()) {
      case 'home':
        return `${match.home_team?.name || 'Home'} Win`;
      case 'away':
        return `${match.away_team?.name || 'Away'} Win`;
      case 'draw':
        return 'Draw';
      default:
        return prediction;
    }
  }

  /**
   * Start periodic refresh for live data
   */
  startLiveUpdates(): void {
    // Refresh live matches every 30 seconds
    setInterval(() => {
      this.apiService.refreshLiveMatches();
    }, 30000);
  }

  /**
   * Stop live updates (for cleanup)
   */
  stopLiveUpdates(): void {
    // TODO: Implement cleanup logic if needed
  }

  /**
   * Generate demo upcoming matches for betting when API has none
   */
  private generateUpcomingMatches(): DashboardMatch[] {
    const now = new Date();
    const today = new Date(now);
    const tomorrow = new Date(now);
    tomorrow.setDate(today.getDate() + 1);
    const dayAfter = new Date(now);
    dayAfter.setDate(today.getDate() + 2);

    return [
      {
        id: 'demo-1',
        leagueId: 'demo-league-1',
        homeTeam: 'Manchester City',
        awayTeam: 'Liverpool',
        homeTeamLogo: '/assets/teams/man-city.png',
        awayTeamLogo: '/assets/teams/liverpool.png',
        kickoff: new Date(today.getFullYear(), today.getMonth(), today.getDate(), 15, 30),
        status: 'upcoming',
        odds: {
          home: 2.10,
          draw: 3.40,
          away: 3.20
        }
      },
      {
        id: 'demo-2',
        leagueId: 'demo-league-1',
        homeTeam: 'Arsenal',
        awayTeam: 'Chelsea',
        homeTeamLogo: '/assets/teams/arsenal.png',
        awayTeamLogo: '/assets/teams/chelsea.png',
        kickoff: new Date(today.getFullYear(), today.getMonth(), today.getDate(), 18, 0),
        status: 'upcoming',
        odds: {
          home: 2.25,
          draw: 3.60,
          away: 2.90
        }
      },
      {
        id: 'demo-3',
        leagueId: 'demo-league-2',
        homeTeam: 'Real Madrid',
        awayTeam: 'Barcelona',
        homeTeamLogo: '/assets/teams/real-madrid.png',
        awayTeamLogo: '/assets/teams/barcelona.png',
        kickoff: new Date(tomorrow.getFullYear(), tomorrow.getMonth(), tomorrow.getDate(), 21, 0),
        status: 'upcoming',
        odds: {
          home: 2.40,
          draw: 3.20,
          away: 2.80
        }
      },
      {
        id: 'demo-4',
        leagueId: 'demo-league-3',
        homeTeam: 'Bayern Munich',
        awayTeam: 'Borussia Dortmund',
        homeTeamLogo: '/assets/teams/bayern.png',
        awayTeamLogo: '/assets/teams/dortmund.png',
        kickoff: new Date(dayAfter.getFullYear(), dayAfter.getMonth(), dayAfter.getDate(), 16, 30),
        status: 'upcoming',
        odds: {
          home: 1.90,
          draw: 3.50,
          away: 3.80
        }
      }
    ];
  }

  /**
   * Generate demo live matches for betting when API has none
   */
  private generateLiveMatches(): DashboardMatch[] {
    return [
      {
        id: 'live-demo-1',
        leagueId: 'demo-league-1',
        homeTeam: 'Tottenham',
        awayTeam: 'Manchester United',
        homeTeamLogo: '/assets/teams/tottenham.png',
        awayTeamLogo: '/assets/teams/man-utd.png',
        kickoff: new Date(Date.now() - 45 * 60 * 1000), // Started 45 minutes ago
        status: 'live',
        homeScore: 1,
        awayScore: 0,
        odds: {
          home: 3.10,
          draw: 3.30,
          away: 2.20
        },
        liveData: {
          minute: 67,
          possession: { home: 58, away: 42 }
        }
      },
      {
        id: 'live-demo-2',
        leagueId: 'demo-league-2',
        homeTeam: 'Atletico Madrid',
        awayTeam: 'Valencia',
        homeTeamLogo: '/assets/teams/atletico.png',
        awayTeamLogo: '/assets/teams/valencia.png',
        kickoff: new Date(Date.now() - 25 * 60 * 1000), // Started 25 minutes ago
        status: 'live',
        homeScore: 2,
        awayScore: 1,
        odds: {
          home: 1.85,
          draw: 3.80,
          away: 4.20
        },
        liveData: {
          minute: 38,
          possession: { home: 65, away: 35 }
        }
      }
    ];
  }
}