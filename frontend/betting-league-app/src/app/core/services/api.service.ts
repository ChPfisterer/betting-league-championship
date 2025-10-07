import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable, BehaviorSubject } from 'rxjs';
import { map } from 'rxjs/operators';
import { environment } from '../../../environments/environment';

// API Response interfaces
export interface Competition {
  id: string;
  name: string;
  sport_id: string;
  season_id: string;
  start_date: string;
  end_date?: string;
  status: 'scheduled' | 'active' | 'completed' | 'cancelled';
  description?: string;
  sport?: Sport;
  season?: Season;
}

export interface Sport {
  id: string;
  name: string;
  description?: string;
  icon?: string;
}

export interface Season {
  id: string;
  name: string;
  year: number;
  start_date: string;
  end_date?: string;
  is_current: boolean;
}

export interface Team {
  id: string;
  name: string;
  country?: string;
  logo_url?: string;
  description?: string;
  founded_year?: number;
}

export interface Match {
  id: string;
  competition_id: string;
  home_team_id: string;
  away_team_id: string;
  match_date: string;
  status: 'scheduled' | 'live' | 'completed' | 'postponed' | 'cancelled';
  home_score?: number;
  away_score?: number;
  venue?: string;
  round?: string;
  competition?: Competition;
  home_team?: Team;
  away_team?: Team;
}

export interface Bet {
  id: string;
  user_id: string;
  match_id: string;
  bet_type: string;
  predicted_outcome: string;
  odds: number;
  stake_amount: number;
  potential_payout: number;
  placed_at: string;
  status: 'pending' | 'won' | 'lost' | 'void';
  match?: Match;
}

export interface UserStats {
  total_bets: number;
  active_bets: number;
  won_bets: number;
  lost_bets: number;
  win_rate: number;
  total_stake: number;
  total_winnings: number;
  net_profit: number;
}

export interface Group {
  id: string;
  name: string;
  description?: string;
  created_at: string;
  is_active: boolean;
}

export interface GroupMembership {
  id: string;
  user_id: string;
  group_id: string;
  joined_at: string;
  is_active: boolean;
  group?: Group;
}

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private readonly baseUrl = environment.apiUrl;
  
  // Real-time data subjects for dashboard updates
  private matchesSubject = new BehaviorSubject<Match[]>([]);
  private userStatsSubject = new BehaviorSubject<UserStats | null>(null);
  private userBetsSubject = new BehaviorSubject<Bet[]>([]);
  
  public matches$ = this.matchesSubject.asObservable();
  public userStats$ = this.userStatsSubject.asObservable();
  public userBets$ = this.userBetsSubject.asObservable();

  constructor(private http: HttpClient) {}

  // Competition APIs
  getCompetitions(): Observable<Competition[]> {
    return this.http.get<Competition[]>(`${this.baseUrl}/api/v1/competitions/`);
  }

  getCompetition(id: string): Observable<Competition> {
    return this.http.get<Competition>(`${this.baseUrl}/api/v1/competitions/${id}`);
  }

  // Match APIs
  getMatches(params?: { 
    competition_id?: string, 
    status?: string, 
    limit?: number,
    offset?: number 
  }): Observable<Match[]> {
    let httpParams = new HttpParams();
    if (params?.competition_id) httpParams = httpParams.set('competition_id', params.competition_id);
    if (params?.status) httpParams = httpParams.set('status', params.status);
    if (params?.limit) httpParams = httpParams.set('limit', params.limit.toString());
    if (params?.offset) httpParams = httpParams.set('offset', params.offset.toString());

    return this.http.get<Match[]>(`${this.baseUrl}/api/v1/matches/`, { params: httpParams });
  }

  getMatch(id: string): Observable<Match> {
    return this.http.get<Match>(`${this.baseUrl}/api/v1/matches/${id}`);
  }

  getLiveMatches(): Observable<Match[]> {
    return this.getMatches({ status: 'live' });
  }

  getUpcomingMatches(limit: number = 10): Observable<Match[]> {
    return this.getMatches({ status: 'scheduled', limit });
  }

  // Team APIs
  getTeams(): Observable<Team[]> {
    return this.http.get<Team[]>(`${this.baseUrl}/api/v1/teams`);
  }

  getTeam(id: string): Observable<Team> {
    return this.http.get<Team>(`${this.baseUrl}/api/v1/teams/${id}`);
  }

  // Betting APIs
  getUserBets(userId: string, params?: { 
    status?: string, 
    limit?: number,
    offset?: number 
  }): Observable<Bet[]> {
    let httpParams = new HttpParams();
    if (params?.status) httpParams = httpParams.set('status', params.status);
    if (params?.limit) httpParams = httpParams.set('limit', params.limit.toString());
    if (params?.offset) httpParams = httpParams.set('offset', params.offset.toString());

    return this.http.get<Bet[]>(`${this.baseUrl}/api/v1/bets/user/${userId}`, { params: httpParams });
  }

  placeBet(betData: {
    match_id: string;
    bet_type: string;
    predicted_outcome: string;
    odds: number;
    stake_amount: number;
  }): Observable<Bet> {
    return this.http.post<Bet>(`${this.baseUrl}/api/v1/bets/`, betData);
  }

  getBet(id: string): Observable<Bet> {
    return this.http.get<Bet>(`${this.baseUrl}/api/v1/bets/${id}`);
  }

  // User Stats API
  getUserStats(userId: string): Observable<UserStats> {
    return this.http.get<UserStats>(`${this.baseUrl}/api/v1/bets/statistics/user/${userId}`);
  }

  // Group APIs
  getUserGroups(userId: string): Observable<GroupMembership[]> {
    return this.http.get<GroupMembership[]>(`${this.baseUrl}/api/v1/group-memberships/user/${userId}/groups`);
  }

  getGroup(id: string): Observable<Group> {
    return this.http.get<Group>(`${this.baseUrl}/api/v1/groups/${id}`);
  }

  // Sports APIs
  getSports(): Observable<Sport[]> {
    return this.http.get<Sport[]>(`${this.baseUrl}/api/v1/sports`);
  }

  // Dashboard-specific methods that combine data and update subjects
  async loadDashboardData(userId: string): Promise<void> {
    try {
      // Load all dashboard data in parallel
      const [matches, userStats, userBets] = await Promise.all([
        this.getMatches({ limit: 20 }).toPromise(),
        this.getUserStats(userId).toPromise(),
        this.getUserBets(userId, { limit: 10 }).toPromise()
      ]);

      // Update subjects with fresh data
      if (matches) this.matchesSubject.next(matches);
      if (userStats) this.userStatsSubject.next(userStats);
      if (userBets) this.userBetsSubject.next(userBets);
      
    } catch (error) {
      console.error('Error loading dashboard data:', error);
      // You might want to show a user-friendly error message here
    }
  }

  // Utility methods for dashboard
  getMatchesByStatus(status: 'live' | 'scheduled' | 'finished'): Observable<Match[]> {
    return this.matches$.pipe(
      map(matches => matches.filter(match => match.status === status))
    );
  }

  getActiveBets(): Observable<Bet[]> {
    return this.userBets$.pipe(
      map(bets => bets.filter(bet => bet.status === 'pending'))
    );
  }

  // Real-time updates (you can expand this for WebSocket integration)
  refreshLiveMatches(): void {
    this.getLiveMatches().subscribe(matches => {
      const currentMatches = this.matchesSubject.value;
      // Update only live matches, keep others
      const updatedMatches = currentMatches.map(match => {
        const liveUpdate = matches.find(live => live.id === match.id);
        return liveUpdate || match;
      });
      this.matchesSubject.next(updatedMatches);
    });
  }
}