import { Injectable } from '@angular/core';
import { environment } from '../../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class FontAwesomeService {
  private kitLoaded = false;

  constructor() {}

  /**
   * Dynamically load FontAwesome kit from environment configuration
   * This avoids hardcoding the kit ID in index.html
   */
  loadFontAwesome(): Promise<void> {
    return new Promise((resolve, reject) => {
      if (this.kitLoaded) {
        resolve();
        return;
      }

      // Get kit ID from environment (can be overridden by environment variables)
      const kitId = environment.fontawesome?.kitId || this.getKitIdFromEnvVar();
      
      if (!kitId) {
        console.warn('FontAwesome kit ID not configured');
        resolve(); // Don't fail the app if FontAwesome isn't available
        return;
      }

      const script = document.createElement('script');
      script.src = `https://kit.fontawesome.com/${kitId}.js`;
      script.crossOrigin = 'anonymous';
      script.async = true;

      script.onload = () => {
        this.kitLoaded = true;
        console.log('FontAwesome kit loaded successfully');
        resolve();
      };

      script.onerror = (error) => {
        console.error('Failed to load FontAwesome kit:', error);
        reject(error);
      };

      document.head.appendChild(script);
    });
  }

  /**
   * Get FontAwesome kit ID from environment variable
   * This allows for runtime configuration without rebuilding
   */
  private getKitIdFromEnvVar(): string | null {
    // Check if running in browser environment
    if (typeof window !== 'undefined' && (window as any).__fontawesome_kit_id) {
      return (window as any).__fontawesome_kit_id;
    }
    return null;
  }

  /**
   * Check if FontAwesome is loaded and available
   */
  isLoaded(): boolean {
    return this.kitLoaded && typeof (window as any).FontAwesome !== 'undefined';
  }
}