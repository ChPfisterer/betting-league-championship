import { Component, Inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule, FormBuilder, FormGroup, Validators } from '@angular/forms';
import { MatDialogModule, MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { MatButtonModule } from '@angular/material/button';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatIconModule } from '@angular/material/icon';
import { MatCardModule } from '@angular/material/card';
import { MatDividerModule } from '@angular/material/divider';
import { MatSliderModule } from '@angular/material/slider';
import { MatChipsModule } from '@angular/material/chips';

export interface BetDialogData {
  match: {
    id: string;
    homeTeam: string;
    awayTeam: string;
    kickoff: Date;
    status: string;
  };
  selectedPrediction: 'home' | 'draw' | 'away';
}

export interface BetPlacementResult {
  matchId: string;
  prediction: 'home' | 'draw' | 'away';
}

@Component({
  selector: 'app-bet-dialog',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    ReactiveFormsModule,
    MatDialogModule,
    MatButtonModule,
    MatFormFieldModule,
    MatInputModule,
    MatIconModule,
    MatCardModule,
    MatDividerModule,
    MatSliderModule,
    MatChipsModule
  ],
  template: `
    <div class="bet-dialog">
      <div class="dialog-header">
        <h2 mat-dialog-title>
          <mat-icon>sports_soccer</mat-icon>
          Make Your Prediction
        </h2>
        <button mat-icon-button (click)="onCancel()" class="close-button">
          <mat-icon>close</mat-icon>
        </button>
      </div>

      <mat-dialog-content>
        <!-- Match Information -->
        <mat-card class="match-info-card">
          <mat-card-content>
            <div class="match-header">
              <div class="teams">
                <span class="team">{{ data.match.homeTeam }}</span>
                <span class="vs">vs</span>
                <span class="team">{{ data.match.awayTeam }}</span>
              </div>
              <div class="match-time">
                {{ data.match.kickoff | date:'medium' }}
              </div>
            </div>

            <!-- Prediction Options -->
            <div class="prediction-options">
              <div class="options-row">
                <button 
                  mat-stroked-button 
                  [class.selected]="selectedPrediction === 'home'"
                  (click)="selectPrediction('home')"
                  class="prediction-option">
                  <div class="option-content">
                    <span class="team-name">{{ data.match.homeTeam }}</span>
                  </div>
                </button>

                <button 
                  mat-stroked-button 
                  [class.selected]="selectedPrediction === 'draw'"
                  (click)="selectPrediction('draw')"
                  class="prediction-option">
                  <div class="option-content">
                    <span class="team-name">Draw</span>
                  </div>
                </button>

                <button 
                  mat-stroked-button 
                  [class.selected]="selectedPrediction === 'away'"
                  (click)="selectPrediction('away')"
                  class="prediction-option">
                  <div class="option-content">
                    <span class="team-name">{{ data.match.awayTeam }}</span>
                  </div>
                </button>
              </div>
            </div>
          </mat-card-content>
        </mat-card>

        <!-- Prediction Summary -->
        <mat-card class="prediction-summary-card" *ngIf="isValidPrediction()">
          <mat-card-header>
            <mat-card-title>
              <mat-icon>preview</mat-icon>
              Your Prediction
            </mat-card-title>
          </mat-card-header>
          <mat-card-content>
            <div class="summary-row">
              <span class="label">You predict:</span>
              <span class="value prediction-text">{{ getPredictionText() }}</span>
            </div>
            <mat-divider></mat-divider>
            <div class="summary-row total">
              <span class="label">Scoring:</span>
              <span class="value potential-points">1 pt (winner) or 3 pts (exact score)</span>
            </div>
          </mat-card-content>
        </mat-card>
      </mat-dialog-content>

      <mat-dialog-actions>
        <div class="dialog-actions">
          <button mat-button (click)="onCancel()" class="cancel-button">
            Cancel
          </button>
          <button 
            mat-raised-button 
            color="primary" 
            (click)="onMakePrediction()"
            [disabled]="!isValidPrediction()"
            class="make-prediction-button">
            <mat-icon>check_circle</mat-icon>
            Submit Prediction
          </button>
        </div>
      </mat-dialog-actions>
    </div>
  `,
  styles: [`
    .bet-dialog {
      width: 100%;
      max-width: 600px;
      max-height: 90vh;
      overflow-y: auto;
    }

    .dialog-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 20px 24px 0 24px;
    }

    .dialog-header h2 {
      margin: 0;
      display: flex;
      align-items: center;
      gap: 8px;
      color: #1976d2;
    }

    .close-button {
      color: #666;
    }

    .match-info-card {
      margin-bottom: 16px;
      background: linear-gradient(135deg, #1976d2, #1565c0);
      color: white;
    }

    .match-header {
      text-align: center;
      margin-bottom: 20px;
    }

    .teams {
      font-size: 20px;
      font-weight: 600;
      margin-bottom: 8px;
    }

    .team {
      color: white;
    }

    .vs {
      margin: 0 12px;
      color: rgba(255, 255, 255, 0.8);
      font-size: 16px;
    }

    .match-time {
      color: rgba(255, 255, 255, 0.9);
      font-size: 14px;
    }

    .prediction-options {
      margin-top: 20px;
    }

    .options-row {
      display: grid;
      grid-template-columns: 1fr 1fr 1fr;
      gap: 8px;
    }

    .prediction-option {
      background: rgba(255, 255, 255, 0.1);
      border: 2px solid rgba(255, 255, 255, 0.3);
      color: white;
      padding: 16px 8px;
      transition: all 0.3s ease;
    }

    .prediction-option:hover {
      background: rgba(255, 255, 255, 0.2);
      border-color: rgba(255, 255, 255, 0.6);
    }

    .prediction-option.selected {
      background: rgba(255, 255, 255, 0.3);
      border-color: white;
      box-shadow: 0 0 10px rgba(255, 255, 255, 0.5);
    }

    .option-content {
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 4px;
    }

    .team-name {
      font-size: 12px;
      font-weight: 500;
    }

    .odds-value {
      font-size: 18px;
      font-weight: 700;
    }

    .prediction-summary-card {
      background: #f8f9fa;
      border: 2px solid #e9ecef;
    }

    .summary-row {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 8px 0;
    }

    .summary-row.total {
      font-weight: 600;
      font-size: 16px;
    }

    .label {
      color: #666;
    }

    .value {
      font-weight: 500;
    }

    .potential-points {
      color: #4caf50;
      font-weight: 600;
      font-size: 1.1em;
    }

    .prediction-text {
      color: #1976d2;
      font-weight: 600;
    }

    .dialog-actions {
      display: flex;
      justify-content: space-between;
      padding: 16px 0;
      width: 100%;
    }

    .make-prediction-button {
      background: #4caf50;
      color: white;
      padding: 12px 24px;
      font-weight: 600;
    }

    .make-prediction-button:disabled {
      background: #ccc;
      color: #666;
    }

    .cancel-button {
      color: #666;
    }

    @media (max-width: 600px) {
      .bet-dialog {
        max-width: 100vw;
        height: 100vh;
        max-height: 100vh;
      }

      .options-row {
        grid-template-columns: 1fr;
        gap: 12px;
      }

      .teams {
        font-size: 18px;
      }

      .dialog-actions {
        flex-direction: column;
        gap: 12px;
      }

      .place-bet-button,
      .cancel-button {
        width: 100%;
      }
    }
  `]
})
export class BetDialogComponent implements OnInit {
  betForm: FormGroup;
  selectedPrediction: 'home' | 'draw' | 'away';

  constructor(
    private fb: FormBuilder,
    private dialogRef: MatDialogRef<BetDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: BetDialogData
  ) {
    this.selectedPrediction = data.selectedPrediction;
    
    this.betForm = this.fb.group({
      // Form for future prediction fields if needed
    });
  }

  ngOnInit(): void {
    // Component is ready
    console.log('Prediction dialog ready');
  }

  selectPrediction(prediction: 'home' | 'draw' | 'away'): void {
    this.selectedPrediction = prediction;
  }

  isValidPrediction(): boolean {
    return this.selectedPrediction !== null;
  }

  getPredictionText(): string {
    switch (this.selectedPrediction) {
      case 'home':
        return this.data.match.homeTeam;
      case 'away':
        return this.data.match.awayTeam;
      case 'draw':
        return 'Draw';
      default:
        return '';
    }
  }

  calculatePotentialPoints(): number {
    // In prediction contest: 1 point for correct outcome, 3 points for exact score
    return 3; // Maximum possible points
  }

  onMakePrediction(): void {
    if (this.isValidPrediction()) {
      const result: BetPlacementResult = {
        matchId: this.data.match.id,
        prediction: this.selectedPrediction
      };

      this.dialogRef.close(result);
    }
  }

  onCancel(): void {
    this.dialogRef.close(null);
  }
}