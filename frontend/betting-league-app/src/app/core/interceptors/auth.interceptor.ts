import { HttpInterceptorFn, HttpErrorResponse, HttpRequest, HttpEvent } from '@angular/common/http';
import { inject } from '@angular/core';
import { throwError, BehaviorSubject, Observable } from 'rxjs';
import { catchError, switchMap, filter, take } from 'rxjs/operators';
import { AuthService } from '../auth/auth.service';

let isRefreshing = false;
let refreshTokenSubject: BehaviorSubject<any> = new BehaviorSubject<any>(null);

export const authInterceptor: HttpInterceptorFn = (req, next) => {
  const authService = inject(AuthService);
  
  // Add auth header if we have a token
  const authReq = addAuthHeader(req, authService);

  return next(authReq).pipe(
    catchError((error: HttpErrorResponse) => {
      // Handle 401 errors by attempting token refresh
      if (error.status === 401 && !req.url.includes('/oauth/')) {
        return handle401Error(authReq, next, authService);
      }
      
      return throwError(() => error);
    })
  );
};

function addAuthHeader(req: HttpRequest<any>, authService: AuthService): HttpRequest<any> {
  const token = authService.getAccessToken();
  
  if (token && !req.url.includes('/oauth/authorize-url')) {
    return req.clone({
      setHeaders: {
        Authorization: `Bearer ${token}`
      }
    });
  }
  
  return req;
}

function handle401Error(req: HttpRequest<any>, next: any, authService: AuthService): Observable<HttpEvent<any>> {
  if (!isRefreshing) {
    isRefreshing = true;
    refreshTokenSubject.next(null);

    return authService.refreshToken().pipe(
      switchMap((tokenResponse: any): Observable<HttpEvent<any>> => {
        isRefreshing = false;
        refreshTokenSubject.next(tokenResponse.access_token);
        
        // Retry the original request with new token
        const newAuthReq = addAuthHeader(req, authService);
        return next(newAuthReq);
      }),
      catchError((error) => {
        isRefreshing = false;
        authService.logout().subscribe();
        return throwError(() => error);
      })
    );
  } else {
    // Wait for token refresh to complete
    return refreshTokenSubject.pipe(
      filter(token => token !== null),
      take(1),
      switchMap((): Observable<HttpEvent<any>> => {
        const newAuthReq = addAuthHeader(req, authService);
        return next(newAuthReq);
      })
    );
  }
}