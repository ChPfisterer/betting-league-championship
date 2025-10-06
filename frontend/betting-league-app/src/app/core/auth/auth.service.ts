import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Router } from '@angular/router';
import { BehaviorSubject, Observable, throwError } from 'rxjs';
import { map, tap, catchError, switchMap } from 'rxjs/operators';
import { jwtDecode } from 'jwt-decode';
import { environment } from '../../../environments/environment';

export interface User {
  id: string;
  username: string;
  email: string;
  firstName: string;
  lastName: string;
  roles: string[];
  isAdmin: boolean;
}

export interface TokenResponse {
  access_token: string;
  refresh_token: string;
  expires_in: number;
  token_type: string;
}

export interface AuthState {
  state: string;
  codeVerifier?: string;
}

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private readonly API_URL = environment.apiUrl;
  private readonly KEYCLOAK_CONFIG = environment.keycloak;
  
  private currentUserSubject = new BehaviorSubject<User | null>(null);
  private isAuthenticatedSubject = new BehaviorSubject<boolean>(false);
  
  public currentUser$ = this.currentUserSubject.asObservable();
  public isAuthenticated$ = this.isAuthenticatedSubject.asObservable();

  constructor(
    private http: HttpClient,
    private router: Router
  ) {
    this.initializeAuthState();
  }

  /**
   * Initialize authentication state from stored tokens
   */
  private initializeAuthState(): void {
    const token = this.getAccessToken();
    if (token && !this.isTokenExpired(token)) {
      this.loadUserInfo().subscribe({
        next: (user) => {
          this.currentUserSubject.next(user);
          this.isAuthenticatedSubject.next(true);
        },
        error: () => {
          this.clearTokens();
        }
      });
    }
  }

  /**
   * Start OAuth login flow
   */
  login(): void {
    this.getAuthorizationUrl().subscribe({
      next: (response) => {
        // Store state for verification
        this.storeAuthState({
          state: response.state
        });
        
        // Redirect to Keycloak
        window.location.href = response.authorize_url;
      },
      error: (error) => {
        console.error('Failed to get authorization URL:', error);
      }
    });
  }

  /**
   * Handle OAuth callback
   */
  handleCallback(code: string, state: string): Observable<User> {
    return this.verifyStateAndExchangeCode(code, state).pipe(
      tap((tokenResponse) => {
        this.storeTokens(tokenResponse);
        this.clearAuthState();
      }),
      switchMap(() => this.loadUserInfo()),
      tap((user: User) => {
        this.currentUserSubject.next(user);
        this.isAuthenticatedSubject.next(true);
      }),
      catchError((error) => {
        console.error('Callback handling failed:', error);
        this.clearTokens();
        return throwError(error);
      })
    );
  }

  /**
   * Logout user
   */
  logout(): Observable<any> {
    const refreshToken = this.getRefreshToken();
    
    if (refreshToken) {
      return this.http.post(`${this.API_URL}/auth/keycloak/oauth/logout`, {
        refresh_token: refreshToken
      }).pipe(
        tap(() => this.performLogout()),
        catchError(() => {
          // Even if logout request fails, clear local state
          this.performLogout();
          return throwError('Logout request failed');
        })
      );
    } else {
      this.performLogout();
      return throwError('No refresh token available');
    }
  }

  /**
   * Refresh access token
   */
  refreshToken(): Observable<TokenResponse> {
    const refreshToken = this.getRefreshToken();
    
    if (!refreshToken) {
      return throwError('No refresh token available');
    }

    return this.http.post<TokenResponse>(`${this.API_URL}/auth/keycloak/oauth/refresh`, {
      refresh_token: refreshToken
    }).pipe(
      tap((tokenResponse) => {
        this.storeTokens(tokenResponse);
      }),
      catchError((error) => {
        console.error('Token refresh failed:', error);
        this.performLogout();
        return throwError(error);
      })
    );
  }

  /**
   * Get current user info
   */
  getCurrentUser(): User | null {
    return this.currentUserSubject.value;
  }

  /**
   * Check if user is authenticated
   */
  isAuthenticated(): boolean {
    return this.isAuthenticatedSubject.value;
  }

  /**
   * Check if user has specific role
   */
  hasRole(role: string): boolean {
    const user = this.getCurrentUser();
    return user?.roles?.includes(role) || false;
  }

  /**
   * Check if user is admin
   */
  isAdmin(): boolean {
    const user = this.getCurrentUser();
    return user?.isAdmin || false;
  }

  // Private methods

  private getAuthorizationUrl(): Observable<{authorize_url: string, state: string}> {
    const params = new HttpParams()
      .set('redirect_uri', `${window.location.origin}/auth/callback`);
    
    return this.http.get<{authorize_url: string, state: string}>(
      `${this.API_URL}/auth/keycloak/oauth/authorize-url`,
      { params }
    );
  }

  private verifyStateAndExchangeCode(code: string, state: string): Observable<TokenResponse> {
    const storedState = this.getStoredAuthState();
    
    if (!storedState || storedState.state !== state) {
      return throwError('Invalid state parameter');
    }

    return this.http.post<TokenResponse>(`${this.API_URL}/auth/keycloak/oauth/token`, {
      code,
      redirect_uri: `${window.location.origin}/auth/callback`,
      state
    });
  }

  private loadUserInfo(): Observable<User> {
    return this.http.get<User>(`${this.API_URL}/auth/keycloak/user/info`);
  }

  private performLogout(): void {
    this.clearTokens();
    this.clearAuthState();
    this.currentUserSubject.next(null);
    this.isAuthenticatedSubject.next(false);
    this.router.navigate(['/']);
  }

  private storeTokens(tokenResponse: TokenResponse): void {
    localStorage.setItem('access_token', tokenResponse.access_token);
    localStorage.setItem('refresh_token', tokenResponse.refresh_token);
    localStorage.setItem('token_expires_at', 
      (Date.now() + (tokenResponse.expires_in * 1000)).toString()
    );
  }

  private clearTokens(): void {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('token_expires_at');
  }

  private storeAuthState(authState: AuthState): void {
    localStorage.setItem('auth_state', JSON.stringify(authState));
  }

  private getStoredAuthState(): AuthState | null {
    const stored = localStorage.getItem('auth_state');
    return stored ? JSON.parse(stored) : null;
  }

  private clearAuthState(): void {
    localStorage.removeItem('auth_state');
  }

  getAccessToken(): string | null {
    return localStorage.getItem('access_token');
  }

  private getRefreshToken(): string | null {
    return localStorage.getItem('refresh_token');
  }

  private isTokenExpired(token: string): boolean {
    try {
      const decoded: any = jwtDecode(token);
      const currentTime = Math.floor(Date.now() / 1000);
      return decoded.exp < currentTime;
    } catch {
      return true;
    }
  }
}