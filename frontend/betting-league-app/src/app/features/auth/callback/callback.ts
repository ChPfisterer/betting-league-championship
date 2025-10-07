import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { AuthService } from '../../../core/auth/auth.service';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-callback',
  standalone: true,
  imports: [CommonModule, MatProgressSpinnerModule, MatCardModule, MatButtonModule],
  templateUrl: './callback.html',
  styleUrls: ['./callback.scss']
})
export class CallbackComponent implements OnInit {
  loading = true;
  error: string | null = null;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private authService: AuthService
  ) {}

  ngOnInit(): void {
    this.route.queryParams.subscribe(params => {
      const code = params['code'];
      const state = params['state'];
      const error = params['error'];

      if (error) {
        this.error = `Authentication failed: ${error}`;
        this.loading = false;
        return;
      }

      if (code && state) {
        this.handleCallback(code, state);
      } else {
        this.error = 'Missing required parameters';
        this.loading = false;
      }
    });
  }

  goHome(): void {
    this.router.navigate(['/']);
  }

  private handleCallback(code: string, state: string): void {
    console.log('Handling authentication callback:', { code: code?.substring(0, 10) + '...', state });
    
    this.authService.handleCallback(code, state).subscribe({
      next: (user) => {
        console.log('Authentication successful:', user);
        this.loading = false;
        
        // Small delay to ensure UI updates, then redirect
        setTimeout(() => {
          // Redirect to intended URL or dashboard
          const redirectUrl = sessionStorage.getItem('redirectUrl') || '/dashboard';
          sessionStorage.removeItem('redirectUrl');
          
          console.log('Redirecting to:', redirectUrl);
          this.router.navigate([redirectUrl]);
        }, 500);
      },
      error: (error) => {
        console.error('Authentication failed:', error);
        this.error = `Authentication failed: ${error.message || error}`;
        this.loading = false;
      }
    });
  }
}
