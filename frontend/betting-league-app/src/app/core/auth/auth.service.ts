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
        // Redirect to Keycloak
        window.location.href = response.authorize_url;
      },
      error: (error) => {
        console.error('Failed to get authorization URL:', error);
      }
    });
  }

  /**
   * Initiate Keycloak OAuth flow
   */
  initiateKeycloakLogin(): void {
    this.login();
  }

  /**
   * Initiate Keycloak registration flow
   */
  initiateKeycloakRegistration(): void {
    this.getAuthorizationUrl().subscribe({
      next: (response) => {
        // Add registration parameter to redirect to Keycloak registration page
        const registrationUrl = response.authorize_url.replace('/auth?', '/registrations?');
        window.location.href = registrationUrl;
      },
      error: (error) => {
        console.error('Failed to get registration URL:', error);
        // Fallback to regular login flow
        this.login();
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
      tap((user) => {
        this.currentUserSubject.next(user);
        this.isAuthenticatedSubject.next(true);
      }),
      catchError((error) => {
        console.error('Authentication failed:', error);
        this.clearTokens();
        return throwError(() => error);
      })
    );
  }

  /**
   * Logout user from both application and Keycloak - FORCE complete logout
   */
  logout(): Observable<any> {
    console.log('AuthService: Starting COMPLETE logout...');
    
    // Always perform local cleanup first
    this.performLogout();
    
    // ALWAYS redirect to Keycloak logout to ensure SSO session ends
    // This is the only way to guarantee complete logout from Keycloak
    this.forceKeycloakLogout();
    
    return new Observable(observer => {
      observer.next(null);
      observer.complete();
    });
  }

  /**
   * Force complete Keycloak logout that ends SSO session
   */
  private forceKeycloakLogout(): void {
    const keycloakLogoutUrl = `${environment.keycloak.url}/realms/${environment.keycloak.realm}/protocol/openid-connect/logout`;
    const redirectUri = `${window.location.origin}/login`;
    
    // Get access token to use as hint
    const accessToken = this.getAccessToken();
    
    // Build logout URL with parameters for ending SSO session
    const params = new URLSearchParams({
      'client_id': environment.keycloak.clientId,
      'post_logout_redirect_uri': redirectUri
    });
    
    // Add session_state and id_token_hint if available to help Keycloak identify session
    if (accessToken) {
      // Use access token as hint (Keycloak may accept this)
      params.append('id_token_hint', accessToken);
    }
    
    // Add additional parameter to help ensure complete logout
    params.append('logout', 'true');
    
    const logoutUrl = `${keycloakLogoutUrl}?${params.toString()}`;
    
    console.log('AuthService: Forcing complete Keycloak SSO logout:', logoutUrl);
    
    // Clear any Keycloak-related cookies before redirect
    this.clearKeycloakCookies();
    
    // Redirect to Keycloak logout
    window.location.href = logoutUrl;
  }

  /**
   * Clear Keycloak-related cookies to help ensure clean logout
   */
  private clearKeycloakCookies(): void {
    // Clear common Keycloak session cookies
    const cookiesToClear = [
      'KEYCLOAK_SESSION',
      'KEYCLOAK_SESSION_LEGACY',
      'KEYCLOAK_IDENTITY',
      'KEYCLOAK_IDENTITY_LEGACY',
      'AUTH_SESSION_ID',
      'AUTH_SESSION_ID_LEGACY'
    ];
    
    cookiesToClear.forEach(cookieName => {
      document.cookie = `${cookieName}=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/; domain=${window.location.hostname}`;
      document.cookie = `${cookieName}=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/; domain=.${window.location.hostname}`;
    });
  }

  /**
   * Redirect to Keycloak logout endpoint with maximum automation
   */
  private logoutFromKeycloak(): void {
    const keycloakLogoutUrl = `${environment.keycloak.url}/realms/${environment.keycloak.realm}/protocol/openid-connect/logout`;
    const redirectUri = `${window.location.origin}/login`;
    
    // Get the access token for logout hint
    const accessToken = this.getAccessToken();
    
    // Build logout URL with parameters for maximum automation
    const params = new URLSearchParams({
      'client_id': environment.keycloak.clientId,
      'post_logout_redirect_uri': redirectUri,
      'redirect_uri': redirectUri  // Some Keycloak versions prefer this
    });
    
    // Add token hint if available for automatic logout
    if (accessToken) {
      params.append('id_token_hint', accessToken);
    }
    
    const logoutUrl = `${keycloakLogoutUrl}?${params.toString()}`;
    
    console.log('AuthService: Redirecting to Keycloak logout (should be automatic):', logoutUrl);
    
    // Redirect to Keycloak logout
    window.location.href = logoutUrl;
  }

  /**
   * Refresh access token
   */
  refreshToken(): Observable<TokenResponse> {
    const refreshToken = this.getRefreshToken();
    
    if (!refreshToken) {
      return throwError(() => 'No refresh token available');
    }

    const body = new URLSearchParams({
      grant_type: 'refresh_token',
      client_id: environment.keycloak.clientId,
      refresh_token: refreshToken
    });

    const headers = {
      'Content-Type': 'application/x-www-form-urlencoded'
    };

    return this.http.post<any>(
      `${environment.keycloak.url}/realms/${environment.keycloak.realm}/protocol/openid-connect/token`,
      body.toString(),
      { headers }
    ).pipe(
      map((response: any) => ({
        access_token: response.access_token,
        refresh_token: response.refresh_token,
        expires_in: response.expires_in,
        token_type: response.token_type
      })),
      tap((tokenResponse) => {
        this.storeTokens(tokenResponse);
      }),
      catchError((error) => {
        console.error('Token refresh failed:', error);
        this.performLogout();
        return throwError(() => error);
      })
    );
  }

  /**
   * Get current user
   */
  getCurrentUser(): User | null {
    return this.currentUserSubject.value;
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
    return new Observable(observer => {
      this.generateAuthUrl().then(result => {
        observer.next(result);
        observer.complete();
      }).catch(error => {
        observer.error(error);
      });
    });
  }

  private async generateAuthUrl(): Promise<{authorize_url: string, state: string}> {
    // Generate state for CSRF protection
    const state = this.generateRandomString(32);
    
    // Generate PKCE code verifier and challenge
    const codeVerifier = this.generateRandomString(128);
    const codeChallenge = await this.base64URLEncode(codeVerifier);
    
    // Store code verifier for later use
    this.storeAuthState({
      state: state,
      codeVerifier: codeVerifier
    });
    
    // Build authorization URL with PKCE
    const params = new URLSearchParams({
      client_id: environment.keycloak.clientId,
      redirect_uri: `${window.location.origin}/auth/callback`,
      response_type: 'code',
      scope: 'openid profile email',
      state: state,
      code_challenge: codeChallenge,
      code_challenge_method: 'S256'
    });

    const authorize_url = `${environment.keycloak.url}/realms/${environment.keycloak.realm}/protocol/openid-connect/auth?${params.toString()}`;
    
    return { authorize_url, state };
  }

  private generateRandomString(length: number): string {
    const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._~';
    let result = '';
    for (let i = 0; i < length; i++) {
      result += chars.charAt(Math.floor(Math.random() * chars.length));
    }
    return result;
  }

  private async base64URLEncode(codeVerifier: string): Promise<string> {
    const encoder = new TextEncoder();
    const data = encoder.encode(codeVerifier);
    const digest = await crypto.subtle.digest('SHA-256', data);
    return btoa(String.fromCharCode(...new Uint8Array(digest)))
      .replace(/\+/g, '-')
      .replace(/\//g, '_')
      .replace(/=/g, '');
  }

  private verifyStateAndExchangeCode(code: string, state: string): Observable<TokenResponse> {
    const storedState = this.getStoredAuthState();
    
    if (!storedState || storedState.state !== state) {
      return throwError(() => 'Invalid state parameter');
    }

    // Exchange code for tokens directly with Keycloak using PKCE
    const bodyParams: any = {
      grant_type: 'authorization_code',
      client_id: environment.keycloak.clientId,
      code: code,
      redirect_uri: `${window.location.origin}/auth/callback`
    };

    // Add PKCE code verifier if available
    if (storedState.codeVerifier) {
      bodyParams.code_verifier = storedState.codeVerifier;
    }

    const body = new URLSearchParams(bodyParams);

    const headers = {
      'Content-Type': 'application/x-www-form-urlencoded'
    };

    return this.http.post<any>(
      `${environment.keycloak.url}/realms/${environment.keycloak.realm}/protocol/openid-connect/token`,
      body.toString(),
      { headers }
    ).pipe(
      map((response: any) => ({
        access_token: response.access_token,
        refresh_token: response.refresh_token,
        expires_in: response.expires_in,
        token_type: response.token_type
      }))
    );
  }

  private loadUserInfo(): Observable<User> {
    const token = this.getAccessToken();
    
    if (!token) {
      return throwError(() => 'No access token available');
    }

    try {
      const decoded: any = jwtDecode(token);
      
      const user: User = {
        id: decoded.sub || '',
        username: decoded.preferred_username || decoded.username || '',
        email: decoded.email || '',
        firstName: decoded.given_name || '',
        lastName: decoded.family_name || '',
        roles: decoded.realm_access?.roles || [],
        isAdmin: decoded.realm_access?.roles?.includes('admin') || false
      };

      return new Observable(observer => {
        observer.next(user);
        observer.complete();
      });
    } catch (error) {
      return throwError(() => 'Invalid access token');
    }
  }

  private performLogout(): void {
    console.log('AuthService: Performing logout cleanup...');
    this.clearTokens();
    this.clearAuthState();
    this.currentUserSubject.next(null);
    this.isAuthenticatedSubject.next(false);
    console.log('AuthService: Logout cleanup complete');
    // Note: Navigation is handled by the calling component
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
      const currentTime = Date.now() / 1000;
      return decoded.exp < currentTime;
    } catch {
      return true;
    }
  }
}