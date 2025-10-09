import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable, BehaviorSubject } from 'rxjs';
import { map, tap, catchError } from 'rxjs/operators';
import { environment } from '../../../environments/environment';
import { AuthService, User } from '../auth/auth.service';

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
  match_date?: string; // For compatibility
  scheduled_at: string; // Actual API field
  status: 'scheduled' | 'live' | 'completed' | 'finished' | 'postponed' | 'cancelled';
  home_score?: number;
  away_score?: number;
  venue?: string;
  round?: string;
  round_number?: number;
  match_type?: 'regular' | 'playoff' | 'final' | 'semifinal' | 'quarterfinal' | 'friendly' | 'qualifier';
  competition?: Competition;
  home_team?: Team;
  away_team?: Team;
  // Temporary additional fields for compatibility with dashboard components
  stage?: string;
  leagueId?: string;
  homeTeam?: string;
  awayTeam?: string;
  homeTeamLogo?: string;
  awayTeamLogo?: string;
  kickoff?: Date;
  liveData?: any;
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
  // Temporary additional fields for compatibility with dashboard components
  prediction?: string;
  stake?: number;
  potentialWin?: number;
  placedAt?: Date;
  pointsEarned?: number;
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

  constructor(
    private http: HttpClient,
    private authService: AuthService
  ) {
    // Subscribe to user changes and automatically clear data when user logs out
    this.authService.currentUser$.subscribe((user: User | null) => {
      if (!user || !user.id) {
        console.log('ApiService: No user or invalid user, clearing data');
        this.clearUserData();
      }
      // Note: We don't automatically load data here to avoid duplicate calls
      // Data loading should be triggered explicitly by components/services
    });
  }

  /**
   * Load all user-specific data
   */
  private loadUserData(userId: string): void {
    console.log('ApiService: Loading user data for:', userId);
    
    // Load user bets
    this.getUserBets(userId).subscribe({
      next: (bets) => {
        console.log('ApiService: Loaded user bets:', bets);
        this.userBetsSubject.next(bets);
      },
      error: (error) => {
        console.error('ApiService: Error loading user bets:', error);
        this.userBetsSubject.next([]);
      }
    });

    // Load user stats
    this.getUserStats(userId).subscribe({
      next: (stats) => {
        console.log('ApiService: Loaded user stats:', stats);
        this.userStatsSubject.next(stats);
      },
      error: (error) => {
        console.error('ApiService: Error loading user stats:', error);
        this.userStatsSubject.next(null);
      }
    });
  }

  /**
   * Clear user data when no user is authenticated
   */
  private clearUserData(): void {
    console.log('ApiService: Clearing user data');
    this.userBetsSubject.next([]);
    this.userStatsSubject.next(null);
  }

  // Competition APIs
  getCompetitions(): Observable<Competition[]> {
    return this.http.get<Competition[]>(`${this.baseUrl}/competitions/`);
  }

  getCompetition(id: string): Observable<Competition> {
    return this.http.get<Competition>(`${this.baseUrl}/competitions/${id}`);
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

    return this.http.get<Match[]>(`${this.baseUrl}/matches/`, { params: httpParams });
  }

  getMatch(id: string): Observable<Match> {
    return this.http.get<Match>(`${this.baseUrl}/matches/${id}`);
  }

  getLiveMatches(): Observable<Match[]> {
    return this.getMatches({ status: 'live' });
  }

  getUpcomingMatches(limit: number = 10): Observable<Match[]> {
    return this.getMatches({ status: 'scheduled', limit });
  }

  // Team APIs
  getTeams(): Observable<Team[]> {
    return this.http.get<Team[]>(`${this.baseUrl}/teams`);
  }

  getTeam(id: string): Observable<Team> {
    return this.http.get<Team>(`${this.baseUrl}/teams/${id}`);
  }

  // Betting APIs
  getUserBets(userId: string, params?: { 
    status?: string, 
    limit?: number,
    offset?: number 
  }): Observable<Bet[]> {
    console.log('ApiService: Getting user bets for user:', userId, 'with params:', params);
    
    let httpParams = new HttpParams();
    if (params?.status) httpParams = httpParams.set('status', params.status);
    if (params?.limit) httpParams = httpParams.set('limit', params.limit.toString());
    if (params?.offset) httpParams = httpParams.set('offset', params.offset.toString());

    const url = `${this.baseUrl}/bets/user/${userId}`;
    console.log('ApiService: Making request to:', url);

    return this.http.get<Bet[]>(url, { params: httpParams }).pipe(
      tap(bets => {
        console.log('ApiService: getUserBets response:', bets);
        console.log('ApiService: getUserBets count:', bets?.length || 0);
      }),
      catchError(error => {
        console.error('ApiService: getUserBets error:', error);
        throw error;
      })
    );
  }

  placeBet(betData: {
    match_id: string;
    outcome?: string;
    predicted_home_score?: number;
    predicted_away_score?: number;
    notes?: string;
    group_id?: string;
  }): Observable<Bet> {
    return this.http.post<Bet>(`${this.baseUrl}/bets/`, betData);
  }

  getBet(id: string): Observable<Bet> {
    return this.http.get<Bet>(`${this.baseUrl}/bets/${id}`);
  }

  // User Stats API
  getUserStats(userId: string): Observable<UserStats> {
    return this.http.get<UserStats>(`${this.baseUrl}/bets/statistics/user/${userId}`);
  }

  // Group APIs
  getUserGroups(userId: string): Observable<GroupMembership[]> {
    return this.http.get<GroupMembership[]>(`${this.baseUrl}/group-memberships/user/${userId}/groups`);
  }

  getGroup(id: string): Observable<Group> {
    return this.http.get<Group>(`${this.baseUrl}/groups/${id}`);
  }

  // Sports APIs
  getSports(): Observable<Sport[]> {
    return this.http.get<Sport[]>(`${this.baseUrl}/sports`);
  }

  // Dashboard-specific methods that combine data and update subjects
  async loadDashboardData(userId: string): Promise<void> {
    try {
      console.log('ApiService: Loading dashboard data for user:', userId);
      console.log('ApiService: User ID type:', typeof userId);
      console.log('ApiService: User ID length:', userId?.length || 0);
      
      // Validate that userId is a proper UUID format
      const uuidRegex = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;
      if (!uuidRegex.test(userId)) {
        console.error('ApiService: Invalid UUID format for user ID:', userId);
        throw new Error(`Invalid user ID format: ${userId}. Expected UUID format.`);
      }
      
      // Load all dashboard data in parallel
      const [matches, userStats, userBets] = await Promise.all([
        this.getMatches({ limit: 20 }).toPromise(),
        this.getUserStats(userId).toPromise(),
        this.getUserBets(userId, { limit: 10 }).toPromise()
      ]);

      console.log('ApiService: Loaded user bets:', userBets);
      console.log('ApiService: User bets count:', userBets?.length || 0);
      console.log('ApiService: Loaded user stats:', userStats);

      // Update subjects with fresh data
      if (matches) this.matchesSubject.next(matches);
      if (userStats) this.userStatsSubject.next(userStats);
      if (userBets) this.userBetsSubject.next(userBets);
      
    } catch (error) {
      console.error('ApiService: Error loading dashboard data:', error);
      // Clear data on error to prevent stale data
      this.clearUserData();
      throw error; // Re-throw to let caller handle the error
    }
  }

  // Utility methods for dashboard
  getMatchesByStatus(status: 'live' | 'scheduled' | 'finished'): Observable<Match[]> {
    // Make direct API call with status filter to get fresh data with team details
    let httpParams = new HttpParams();
    httpParams = httpParams.set('status', status);
    httpParams = httpParams.set('limit', '100'); // Increased to get all matches (64 FIFA World Cup matches)
    
    return this.http.get<Match[]>(`${this.baseUrl}/matches/`, { params: httpParams });
  }

  /**
   * Get matches with pagination support
   */
  getMatchesByStatusPaginated(
    status: 'live' | 'scheduled' | 'finished',
    skip: number = 0,
    limit: number = 100
  ): Observable<Match[]> {
    let httpParams = new HttpParams();
    httpParams = httpParams.set('status', status);
    httpParams = httpParams.set('skip', skip.toString());
    httpParams = httpParams.set('limit', limit.toString());
    
    return this.http.get<Match[]>(`${this.baseUrl}/matches/`, { params: httpParams });
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

  // User registration
  register(userData: {
    firstName: string;
    lastName: string;
    username: string;
    email: string;
    password: string;
  }): Observable<any> {
    return this.http.post(`${this.baseUrl}/auth/register`, {
      first_name: userData.firstName,
      last_name: userData.lastName,
      username: userData.username,
      email: userData.email,
      password: userData.password
    });
  }
}