import { Component, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatDividerModule } from '@angular/material/divider';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatSnackBarModule, MatSnackBar } from '@angular/material/snack-bar';
import { MatTooltipModule } from '@angular/material/tooltip';
import { MatChipsModule } from '@angular/material/chips';
import { Subscription } from 'rxjs';
import { AuthService, User } from '../../core/auth/auth.service';

@Component({
  selector: 'app-profile',
  standalone: true,
  imports: [
    CommonModule,
    MatCardModule,
    MatButtonModule,
    MatIconModule,
    MatDividerModule,
    MatProgressSpinnerModule,
    MatSnackBarModule,
    MatTooltipModule,
    MatChipsModule
  ],
  template: `
    <div class="profile-container">
      <!-- Header -->
      <div class="profile-header">
        <button mat-icon-button (click)="goBack()" class="back-button">
          <mat-icon>arrow_back</mat-icon>
        </button>
        <h1>My Profile</h1>
      </div>

      <!-- Loading State -->
      <div *ngIf="isLoading" class="loading-container">
        <mat-spinner></mat-spinner>
        <p>Loading profile...</p>
      </div>

      <!-- Profile Content -->
      <div *ngIf="!isLoading" class="profile-content">
        
        <!-- User Information Card -->
        <mat-card class="user-info-card">
          <mat-card-header>
            <div class="user-avatar" mat-card-avatar>
              <mat-icon>person</mat-icon>
            </div>
            <mat-card-title>{{ currentUser?.firstName || 'User' }} {{ currentUser?.lastName || '' }}</mat-card-title>
            <mat-card-subtitle>{{ currentUser?.email || 'No email provided' }}</mat-card-subtitle>
          </mat-card-header>

          <mat-card-content>
            <div class="user-details">
              <div class="detail-item">
                <mat-icon>account_circle</mat-icon>
                <div class="detail-content">
                  <span class="detail-label">Username</span>
                  <span class="detail-value">{{ currentUser?.username || 'Not set' }}</span>
                </div>
              </div>

              <div class="detail-item">
                <mat-icon>email</mat-icon>
                <div class="detail-content">
                  <span class="detail-label">Email Address</span>
                  <span class="detail-value">{{ currentUser?.email || 'Not provided' }}</span>
                </div>
              </div>

              <div class="detail-item">
                <mat-icon>badge</mat-icon>
                <div class="detail-content">
                  <span class="detail-label">User ID</span>
                  <span class="detail-value">{{ currentUser?.id || 'N/A' }}</span>
                </div>
              </div>

              <div class="detail-item">
                <mat-icon>security</mat-icon>
                <div class="detail-content">
                  <span class="detail-label">Roles</span>
                  <div class="roles-container">
                    <mat-chip *ngFor="let role of currentUser?.roles" class="role-chip">
                      {{ role }}
                    </mat-chip>
                    <span *ngIf="!currentUser?.roles?.length" class="no-roles">
                      No roles assigned
                    </span>
                  </div>
                </div>
              </div>

              <div class="detail-item">
                <mat-icon>admin_panel_settings</mat-icon>
                <div class="detail-content">
                  <span class="detail-label">Admin Status</span>
                  <mat-chip [class]="currentUser?.isAdmin ? 'admin-chip' : 'user-chip'">
                    {{ currentUser?.isAdmin ? 'Administrator' : 'Regular User' }}
                  </mat-chip>
                </div>
              </div>
            </div>
          </mat-card-content>
        </mat-card>

        <!-- Authentication Status Card -->
        <mat-card class="auth-status-card">
          <mat-card-header>
            <mat-card-title>
              <mat-icon>verified_user</mat-icon>
              Authentication Status
            </mat-card-title>
          </mat-card-header>

          <mat-card-content>
            <div class="auth-status">
              <div class="status-item">
                <mat-icon class="status-icon success">check_circle</mat-icon>
                <span>Successfully authenticated via Keycloak</span>
              </div>
              
              <div class="status-item">
                <mat-icon class="status-icon success">token</mat-icon>
                <span>Valid access token present</span>
              </div>

              <div class="status-item" *ngIf="isAuthenticated">
                <mat-icon class="status-icon success">schedule</mat-icon>
                <span>Session active</span>
              </div>
            </div>
          </mat-card-content>
        </mat-card>

        <!-- Actions Card -->
        <mat-card class="actions-card">
          <mat-card-header>
            <mat-card-title>
              <mat-icon>settings</mat-icon>
              Account Actions
            </mat-card-title>
          </mat-card-header>

          <mat-card-content>
            <div class="action-buttons">
              <button mat-raised-button color="primary" (click)="refreshProfile()" [disabled]="isRefreshing">
                <mat-spinner diameter="20" *ngIf="isRefreshing"></mat-spinner>
                <mat-icon *ngIf="!isRefreshing">refresh</mat-icon>
                {{ isRefreshing ? 'Refreshing...' : 'Refresh Profile' }}
              </button>

              <button mat-stroked-button color="accent" (click)="viewDashboard()">
                <mat-icon>dashboard</mat-icon>
                Back to Dashboard
              </button>

              <button mat-stroked-button color="warn" (click)="testAuthStatus()">
                <mat-icon>bug_report</mat-icon>
                Test Auth Status
              </button>
            </div>
          </mat-card-content>
        </mat-card>

        <!-- Logout Card -->
        <mat-card class="logout-card">
          <mat-card-header>
            <mat-card-title class="logout-title">
              <mat-icon>logout</mat-icon>
              Sign Out
            </mat-card-title>
            <mat-card-subtitle>End your current session</mat-card-subtitle>
          </mat-card-header>

          <mat-card-content>
            <p class="logout-description">
              This will log you out of the betting platform and redirect you to the Keycloak logout page.
              You'll need to sign in again to access your account.
            </p>

            <div class="logout-actions">
              <button mat-raised-button 
                      color="warn" 
                      class="logout-button"
                      (click)="logout()"
                      [disabled]="isLoggingOut">
                <mat-spinner diameter="20" *ngIf="isLoggingOut"></mat-spinner>
                <mat-icon *ngIf="!isLoggingOut">logout</mat-icon>
                {{ isLoggingOut ? 'Signing Out...' : 'Sign Out' }}
              </button>

              <button mat-button 
                      color="primary" 
                      (click)="quickLogout()"
                      [disabled]="isLoggingOut"
                      matTooltip="Clear local session only">
                <mat-icon>clear</mat-icon>
                Quick Logout
              </button>
            </div>
          </mat-card-content>
        </mat-card>

        <!-- Debug Information (for testing) -->
        <mat-card class="debug-card" *ngIf="showDebugInfo">
          <mat-card-header>
            <mat-card-title>
              <mat-icon>code</mat-icon>
              Debug Information
            </mat-card-title>
          </mat-card-header>

          <mat-card-content>
            <div class="debug-section">
              <h4>Current User Object:</h4>
              <pre class="debug-output">{{ currentUser | json }}</pre>
            </div>

            <div class="debug-section">
              <h4>Authentication State:</h4>
              <pre class="debug-output">{{ debugAuthState | json }}</pre>
            </div>

            <button mat-button (click)="showDebugInfo = false">
              <mat-icon>visibility_off</mat-icon>
              Hide Debug Info
            </button>
          </mat-card-content>
        </mat-card>

        <div class="debug-toggle">
          <button mat-icon-button 
                  (click)="showDebugInfo = !showDebugInfo"
                  matTooltip="Toggle debug information">
            <mat-icon>{{ showDebugInfo ? 'bug_report' : 'code' }}</mat-icon>
          </button>
        </div>
      </div>
    </div>
  `,
  styles: [`
    .profile-container {
      max-width: 800px;
      margin: 0 auto;
      padding: 20px;
      background: transparent;  /* Let app-content handle background */
      min-height: calc(100vh - 120px);  /* Account for header and footer */
      box-sizing: border-box;
    }

    .profile-header {
      display: flex;
      align-items: center;
      margin-bottom: 24px;
      gap: 16px;
      position: relative;
      z-index: 1;
    }

    .profile-header h1 {
      margin: 0;
      color: #333;
      font-weight: 600;
    }

    .back-button {
      color: #667eea;
    }

    .loading-container {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      padding: 60px 20px;
      text-align: center;
    }

    .profile-content {
      display: flex;
      flex-direction: column;
      gap: 24px;
    }

    .user-info-card {
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white;
    }

    .user-info-card mat-card-title {
      color: white;
      font-size: 24px;
      font-weight: 600;
    }

    .user-info-card mat-card-subtitle {
      color: rgba(255, 255, 255, 0.8);
    }

    .user-avatar {
      background-color: rgba(255, 255, 255, 0.2);
      border-radius: 50%;
      width: 60px;
      height: 60px;
      display: flex;
      align-items: center;
      justify-content: center;
    }

    .user-avatar mat-icon {
      font-size: 32px;
      width: 32px;
      height: 32px;
      color: white;
    }

    .user-details {
      margin-top: 20px;
    }

    .detail-item {
      display: flex;
      align-items: flex-start;
      gap: 16px;
      margin-bottom: 20px;
    }

    .detail-item mat-icon {
      color: rgba(255, 255, 255, 0.8);
      margin-top: 2px;
    }

    .detail-content {
      display: flex;
      flex-direction: column;
      flex: 1;
    }

    .detail-label {
      font-size: 14px;
      color: rgba(255, 255, 255, 0.7);
      margin-bottom: 4px;
      font-weight: 500;
    }

    .detail-value {
      color: white;
      font-weight: 500;
    }

    .roles-container {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      margin-top: 4px;
    }

    .role-chip {
      background-color: rgba(255, 255, 255, 0.2);
      color: white;
      font-size: 12px;
    }

    .admin-chip {
      background-color: #ff9800;
      color: white;
    }

    .user-chip {
      background-color: #4caf50;
      color: white;
    }

    .no-roles {
      color: rgba(255, 255, 255, 0.6);
      font-style: italic;
    }

    .auth-status-card mat-card-title {
      display: flex;
      align-items: center;
      gap: 8px;
      color: #4caf50;
    }

    .auth-status {
      display: flex;
      flex-direction: column;
      gap: 16px;
    }

    .status-item {
      display: flex;
      align-items: center;
      gap: 12px;
    }

    .status-icon.success {
      color: #4caf50;
    }

    .actions-card mat-card-title {
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .action-buttons {
      display: flex;
      flex-wrap: wrap;
      gap: 12px;
    }

    .logout-card {
      border: 2px solid #f44336;
    }

    .logout-title {
      color: #f44336;
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .logout-description {
      color: #666;
      line-height: 1.5;
      margin-bottom: 20px;
    }

    .logout-actions {
      display: flex;
      gap: 12px;
      flex-wrap: wrap;
    }

    .logout-button {
      background-color: #f44336;
      color: white;
    }

    .debug-card {
      background-color: #263238;
      color: #e0f2f1;
    }

    .debug-card mat-card-title {
      color: #4db6ac;
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .debug-section {
      margin-bottom: 20px;
    }

    .debug-section h4 {
      color: #4db6ac;
      margin-bottom: 8px;
    }

    .debug-output {
      background-color: #37474f;
      padding: 12px;
      border-radius: 4px;
      font-size: 12px;
      overflow-x: auto;
      white-space: pre-wrap;
      color: #b0bec5;
    }

    .debug-toggle {
      position: fixed;
      bottom: 20px;
      right: 20px;
      z-index: 1000;
    }

    .debug-toggle button {
      background-color: #667eea;
      color: white;
    }

    @media (max-width: 600px) {
      .profile-container {
        padding: 16px;
      }

      .action-buttons,
      .logout-actions {
        flex-direction: column;
      }

      .action-buttons button,
      .logout-actions button {
        width: 100%;
      }
    }
  `]
})
export class ProfileComponent implements OnInit, OnDestroy {
  currentUser: User | null = null;
  isAuthenticated = false;
  isLoading = false;
  isRefreshing = false;
  isLoggingOut = false;
  showDebugInfo = false;
  debugAuthState: any = {};

  private subscriptions: Subscription[] = [];

  constructor(
    private authService: AuthService,
    private router: Router,
    private snackBar: MatSnackBar
  ) {}

  ngOnInit(): void {
    console.log('ProfileComponent: Initializing...');
    this.loadProfile();
    this.subscribeToAuthState();
    console.log('ProfileComponent: Initialization complete');
  }

  ngOnDestroy(): void {
    this.subscriptions.forEach(sub => sub.unsubscribe());
  }

  private loadProfile(): void {
    console.log('ProfileComponent: Loading profile...');
    this.isLoading = true;
    
    // Get current user
    this.currentUser = this.authService.getCurrentUser();
    console.log('ProfileComponent: Current user:', this.currentUser);
    
    // Update debug state
    this.updateDebugState();
    
    this.isLoading = false;
    console.log('ProfileComponent: Profile loaded');
  }

  private subscribeToAuthState(): void {
    this.subscriptions.push(
      this.authService.isAuthenticated$.subscribe((isAuth: boolean) => {
        this.isAuthenticated = isAuth;
        if (!isAuth) {
          this.router.navigate(['/login']);
        }
        this.updateDebugState();
      })
    );

    this.subscriptions.push(
      this.authService.currentUser$.subscribe((user: User | null) => {
        this.currentUser = user;
        this.updateDebugState();
      })
    );
  }

  private updateDebugState(): void {
    this.debugAuthState = {
      isAuthenticated: this.isAuthenticated,
      hasUser: !!this.currentUser,
      timestamp: new Date().toISOString()
    };
  }

  refreshProfile(): void {
    this.isRefreshing = true;
    
    // Simulate refresh - in real app, this would reload user data from API
    setTimeout(() => {
      this.loadProfile();
      this.isRefreshing = false;
      this.snackBar.open('Profile refreshed successfully', 'Close', {
        duration: 3000
      });
    }, 1000);
  }

  testAuthStatus(): void {
    const user = this.authService.getCurrentUser();
    const isAuth = this.isAuthenticated;
    
    let message = `Auth Status: ${isAuth ? 'Authenticated' : 'Not Authenticated'}`;
    if (user) {
      message += ` | User: ${user.username || user.email}`;
    }
    
    this.snackBar.open(message, 'Close', {
      duration: 5000
    });
  }

  logout(): void {
    this.isLoggingOut = true;
    
    this.authService.logout().subscribe({
      next: () => {
        console.log('Profile: Logout initiated (Keycloak will handle redirect)');
        // Note: Keycloak will redirect back to login page
      },
      error: (error) => {
        console.error('Logout error:', error);
        this.isLoggingOut = false;
        
        // Fallback navigation if Keycloak redirect fails
        this.snackBar.open('Logout completed (with errors)', 'Close', {
          duration: 3000
        });
        this.router.navigate(['/login']);
      }
    });
  }

  quickLogout(): void {
    // Clear local session without calling Keycloak logout
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    
    this.snackBar.open('Local session cleared', 'Close', {
      duration: 3000
    });
    
    this.router.navigate(['/login']);
  }

  goBack(): void {
    this.router.navigate(['/dashboard']);
  }

  viewDashboard(): void {
    this.router.navigate(['/dashboard']);
  }
}