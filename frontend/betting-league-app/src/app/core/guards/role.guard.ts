import { Injectable } from '@angular/core';
import { CanActivate, Router, ActivatedRouteSnapshot } from '@angular/router';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { AuthService } from '../auth/auth.service';

@Injectable({
  providedIn: 'root'
})
export class RoleGuard implements CanActivate {
  
  constructor(
    private authService: AuthService,
    private router: Router
  ) {}

  canActivate(route: ActivatedRouteSnapshot): Observable<boolean> | Promise<boolean> | boolean {
    const requiredRoles = route.data['roles'] as string[];
    const requireAdmin = route.data['requireAdmin'] as boolean;
    
    return this.authService.currentUser$.pipe(
      map(user => {
        if (!user) {
          this.router.navigate(['/']);
          return false;
        }

        // Check admin requirement
        if (requireAdmin && !user.isAdmin) {
          this.router.navigate(['/unauthorized']);
          return false;
        }

        // Check specific roles
        if (requiredRoles && requiredRoles.length > 0) {
          const hasRequiredRole = requiredRoles.some(role => user.roles.includes(role));
          if (!hasRequiredRole) {
            this.router.navigate(['/unauthorized']);
            return false;
          }
        }

        return true;
      })
    );
  }
}