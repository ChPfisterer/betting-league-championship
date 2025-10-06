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
    this.authService.handleCallback(code, state).subscribe({
      next: (user) => {
        console.log('Authentication successful:', user);
        
        // Redirect to intended URL or dashboard
        const redirectUrl = sessionStorage.getItem('redirectUrl') || '/dashboard';
        sessionStorage.removeItem('redirectUrl');
        
        this.router.navigate([redirectUrl]);
      },
      error: (error) => {
        console.error('Authentication failed:', error);
        this.error = 'Authentication failed. Please try again.';
        this.loading = false;
      }
    });
  }
}
