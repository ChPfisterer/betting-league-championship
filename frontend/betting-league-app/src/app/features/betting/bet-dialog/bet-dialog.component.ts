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
}

export interface BetPlacementResult {
  matchId: string;
  prediction: 'home' | 'draw' | 'away';
  predictedHomeScore?: number | null;
  predictedAwayScore?: number | null;
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
          <i class="fas fa-futbol"></i>
          Make Your Prediction
        </h2>
        <button mat-icon-button (click)="onCancel()" class="close-button">
          <i class="fas fa-times"></i>
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

          </mat-card-content>
        </mat-card>

        <!-- Score Prediction -->
        <mat-card class="score-prediction-card">
          <mat-card-header>
            <mat-card-title>
              <i class="fas fa-calculator"></i>
              Score Prediction
            </mat-card-title>
            <mat-card-subtitle>Enter the final score to make your prediction</mat-card-subtitle>
          </mat-card-header>
          <mat-card-content>
            <div class="score-inputs" [formGroup]="betForm">
              <div class="score-input-row">
                <div class="team-score-input">
                  <label class="score-label">{{ data.match.homeTeam }}</label>
                  <mat-form-field appearance="outline" class="score-field">
                    <input 
                      matInput 
                      type="number" 
                      min="0" 
                      max="20" 
                      formControlName="homeScore"
                      (input)="onScoreChange()"
                      placeholder="0">
                  </mat-form-field>
                </div>
                
                <div class="vs-separator">
                  <span>-</span>
                </div>
                
                <div class="team-score-input">
                  <label class="score-label">{{ data.match.awayTeam }}</label>
                  <mat-form-field appearance="outline" class="score-field">
                    <input 
                      matInput 
                      type="number" 
                      min="0" 
                      max="20" 
                      formControlName="awayScore"
                      (input)="onScoreChange()"
                      placeholder="0">
                  </mat-form-field>
                </div>
              </div>
              
              <div class="score-hint" *ngIf="hasValidScores()">
                <i class="fas fa-check-circle text-primary"></i>
                <span>Predicting {{ data.match.homeTeam }} {{ predictedHomeScore }} - {{ predictedAwayScore }} {{ data.match.awayTeam }}</span>
              </div>
            </div>
          </mat-card-content>
        </mat-card>

        <!-- Prediction Summary -->
        <mat-card class="prediction-summary-card" *ngIf="isValidPrediction()">>
          <mat-card-header>
            <mat-card-title>
              <i class="fas fa-eye"></i>
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
              <span class="value potential-points">3 points (exact score prediction)</span>
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
            <i class="fas fa-check-circle"></i>
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

    .score-prediction-card {
      margin: 16px 0;
      background: #f8f9fa;
      border: 1px solid #e9ecef;
    }

    .score-toggle {
      margin-bottom: 16px;
    }

    .toggle-score-button {
      color: #1976d2;
      border: 1px solid #1976d2;
      background: transparent;
      transition: all 0.3s ease;
    }

    .toggle-score-button.active {
      background: #1976d2;
      color: white;
    }

    .score-inputs {
      margin-top: 16px;
    }

    .score-input-row {
      display: flex;
      align-items: end;
      gap: 16px;
      justify-content: center;
      margin-bottom: 16px;
    }

    .team-score-input {
      display: flex;
      flex-direction: column;
      align-items: center;
      min-width: 120px;
    }

    .score-label {
      font-size: 14px;
      font-weight: 500;
      margin-bottom: 8px;
      color: #333;
      text-align: center;
    }

    .score-field {
      width: 80px;
    }

    .score-field ::ng-deep .mat-mdc-form-field-subscript-wrapper {
      display: none;
    }

    .score-field ::ng-deep .mat-mdc-text-field-wrapper {
      background: white;
    }

    .score-field input {
      text-align: center;
      font-size: 18px;
      font-weight: bold;
    }

    .vs-separator {
      display: flex;
      align-items: center;
      font-size: 24px;
      font-weight: bold;
      color: #666;
      margin: 0 8px;
      margin-top: 24px;
    }

    .score-hint {
      display: flex;
      align-items: center;
      gap: 8px;
      padding: 12px;
      background: #e8f5e8;
      border-radius: 8px;
      color: #2e7d32;
      font-size: 14px;
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
  predictedHomeScore: number | null = null;
  predictedAwayScore: number | null = null;

  constructor(
    private fb: FormBuilder,
    private dialogRef: MatDialogRef<BetDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: BetDialogData
  ) {
    this.betForm = this.fb.group({
      homeScore: [null, [Validators.required, Validators.min(0), Validators.max(20)]],
      awayScore: [null, [Validators.required, Validators.min(0), Validators.max(20)]]
    });
  }

  ngOnInit(): void {
    // Component is ready
    console.log('Score prediction dialog ready');
  }

  // Derive winner from scores
  get selectedPrediction(): 'home' | 'draw' | 'away' {
    const homeScore = this.predictedHomeScore;
    const awayScore = this.predictedAwayScore;
    
    if (homeScore === null || awayScore === null) {
      return 'home'; // Default, but validation will prevent submission
    }
    
    if (homeScore > awayScore) {
      return 'home';
    } else if (awayScore > homeScore) {
      return 'away';
    } else {
      return 'draw';
    }
  }

  isValidPrediction(): boolean {
    return this.betForm.valid && 
           this.predictedHomeScore !== null && 
           this.predictedAwayScore !== null;
  }

  onScoreChange(): void {
    const homeScore = this.betForm.get('homeScore')?.value;
    const awayScore = this.betForm.get('awayScore')?.value;
    
    this.predictedHomeScore = homeScore !== null && homeScore !== '' ? Number(homeScore) : null;
    this.predictedAwayScore = awayScore !== null && awayScore !== '' ? Number(awayScore) : null;
  }

  hasValidScores(): boolean {
    return this.predictedHomeScore !== null && this.predictedAwayScore !== null &&
           this.predictedHomeScore >= 0 && this.predictedAwayScore >= 0;
  }

  getPredictionText(): string {
    if (this.predictedHomeScore === null || this.predictedAwayScore === null) {
      return 'Enter scores to make prediction';
    }
    
    const winner = this.selectedPrediction;
    const scoreText = `${this.predictedHomeScore} - ${this.predictedAwayScore}`;
    
    switch (winner) {
      case 'home':
        return `${this.data.match.homeTeam} wins (${scoreText})`;
      case 'away':
        return `${this.data.match.awayTeam} wins (${scoreText})`;
      case 'draw':
        return `Draw (${scoreText})`;
      default:
        return scoreText;
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
        prediction: this.selectedPrediction,
        predictedHomeScore: this.predictedHomeScore,
        predictedAwayScore: this.predictedAwayScore
      };

      this.dialogRef.close(result);
    }
  }

  onCancel(): void {
    this.dialogRef.close(null);
  }
}