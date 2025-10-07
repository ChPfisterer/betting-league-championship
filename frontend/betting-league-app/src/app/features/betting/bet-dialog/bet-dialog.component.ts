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
    odds: {
      home: number;
      draw: number;
      away: number;
    };
    status: string;
  };
  selectedPrediction: 'home' | 'draw' | 'away';
}

export interface BetPlacementResult {
  matchId: string;
  prediction: 'home' | 'draw' | 'away';
  odds: number;
  stake: number;
  potentialWin: number;
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
          Place Your Bet
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

            <!-- Betting Options -->
            <div class="betting-options">
              <div class="odds-row">
                <button 
                  mat-stroked-button 
                  [class.selected]="selectedPrediction === 'home'"
                  (click)="selectPrediction('home')"
                  class="odds-option">
                  <div class="odds-content">
                    <span class="team-name">{{ data.match.homeTeam }}</span>
                    <span class="odds-value">{{ data.match.odds.home | number:'1.2-2' }}</span>
                  </div>
                </button>

                <button 
                  mat-stroked-button 
                  [class.selected]="selectedPrediction === 'draw'"
                  (click)="selectPrediction('draw')"
                  class="odds-option">
                  <div class="odds-content">
                    <span class="team-name">Draw</span>
                    <span class="odds-value">{{ data.match.odds.draw | number:'1.2-2' }}</span>
                  </div>
                </button>

                <button 
                  mat-stroked-button 
                  [class.selected]="selectedPrediction === 'away'"
                  (click)="selectPrediction('away')"
                  class="odds-option">
                  <div class="odds-content">
                    <span class="team-name">{{ data.match.awayTeam }}</span>
                    <span class="odds-value">{{ data.match.odds.away | number:'1.2-2' }}</span>
                  </div>
                </button>
              </div>
            </div>
          </mat-card-content>
        </mat-card>

        <!-- Bet Amount Selection -->
        <mat-card class="stake-card">
          <mat-card-header>
            <mat-card-title>Bet Amount</mat-card-title>
          </mat-card-header>
          <mat-card-content>
            <form [formGroup]="betForm">
              <!-- Quick Stake Buttons -->
              <div class="quick-stakes">
                <mat-chip-listbox>
                  <mat-chip-option 
                    *ngFor="let amount of quickStakeAmounts" 
                    (click)="setStake(amount)"
                    [selected]="betForm.get('stake')?.value === amount">
                    €{{ amount }}
                  </mat-chip-option>
                </mat-chip-listbox>
              </div>

              <!-- Custom Stake Input -->
              <mat-form-field appearance="outline" class="stake-input">
                <mat-label>Stake Amount (EUR)</mat-label>
                <input 
                  matInput 
                  type="number" 
                  formControlName="stake"
                  min="1"
                  max="1000"
                  step="0.01"
                  placeholder="Enter amount">
                <mat-icon matSuffix>euro</mat-icon>
                <mat-error *ngIf="betForm.get('stake')?.hasError('required')">
                  Stake amount is required
                </mat-error>
                <mat-error *ngIf="betForm.get('stake')?.hasError('min')">
                  Minimum stake is €1
                </mat-error>
                <mat-error *ngIf="betForm.get('stake')?.hasError('max')">
                  Maximum stake is €1000
                </mat-error>
              </mat-form-field>

              <!-- Stake Slider -->
              <div class="stake-slider-container">
                <mat-slider 
                  min="1" 
                  max="100" 
                  step="1" 
                  discrete
                  [value]="betForm.get('stake')?.value || 1"
                  (input)="onSliderChange($event)">
                  <input matSliderThumb>
                </mat-slider>
              </div>
            </form>
          </mat-card-content>
        </mat-card>

        <!-- Bet Summary -->
        <mat-card class="bet-summary-card" *ngIf="isValidBet()">
          <mat-card-header>
            <mat-card-title>
              <mat-icon>calculate</mat-icon>
              Bet Summary
            </mat-card-title>
          </mat-card-header>
          <mat-card-content>
            <div class="summary-row">
              <span class="label">Selection:</span>
              <span class="value">{{ getPredictionText() }} @ {{ getSelectedOdds() | number:'1.2-2' }}</span>
            </div>
            <div class="summary-row">
              <span class="label">Stake:</span>
              <span class="value">€{{ betForm.get('stake')?.value | number:'1.2-2' }}</span>
            </div>
            <mat-divider></mat-divider>
            <div class="summary-row total">
              <span class="label">Potential Win:</span>
              <span class="value potential-win">€{{ calculatePotentialWin() | number:'1.2-2' }}</span>
            </div>
            <div class="summary-row">
              <span class="label">Net Profit:</span>
              <span class="value net-profit">€{{ calculateNetProfit() | number:'1.2-2' }}</span>
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
            (click)="onPlaceBet()"
            [disabled]="!isValidBet()"
            class="place-bet-button">
            <mat-icon>sports</mat-icon>
            Place Bet - €{{ betForm.get('stake')?.value | number:'1.2-2' }}
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

    .betting-options {
      margin-top: 20px;
    }

    .odds-row {
      display: grid;
      grid-template-columns: 1fr 1fr 1fr;
      gap: 8px;
    }

    .odds-option {
      background: rgba(255, 255, 255, 0.1);
      border: 2px solid rgba(255, 255, 255, 0.3);
      color: white;
      padding: 16px 8px;
      transition: all 0.3s ease;
    }

    .odds-option:hover {
      background: rgba(255, 255, 255, 0.2);
      border-color: rgba(255, 255, 255, 0.6);
    }

    .odds-option.selected {
      background: rgba(255, 255, 255, 0.3);
      border-color: white;
      box-shadow: 0 0 10px rgba(255, 255, 255, 0.5);
    }

    .odds-content {
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

    .stake-card {
      margin-bottom: 16px;
    }

    .quick-stakes {
      margin-bottom: 16px;
    }

    .quick-stakes mat-chip-listbox {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
    }

    .stake-input {
      width: 100%;
      margin-bottom: 16px;
    }

    .stake-slider-container {
      margin-bottom: 16px;
    }

    .bet-summary-card {
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

    .potential-win {
      color: #4caf50;
      font-weight: 700;
    }

    .net-profit {
      color: #2e7d32;
      font-weight: 600;
    }

    .dialog-actions {
      display: flex;
      justify-content: space-between;
      padding: 16px 0;
      width: 100%;
    }

    .place-bet-button {
      background: #4caf50;
      color: white;
      padding: 12px 24px;
      font-weight: 600;
    }

    .place-bet-button:disabled {
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

      .odds-row {
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
  quickStakeAmounts = [5, 10, 20, 50, 100];

  constructor(
    private fb: FormBuilder,
    private dialogRef: MatDialogRef<BetDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: BetDialogData
  ) {
    this.selectedPrediction = data.selectedPrediction;
    
    this.betForm = this.fb.group({
      stake: [10, [Validators.required, Validators.min(1), Validators.max(1000)]]
    });
  }

  ngOnInit(): void {
    // Auto-focus on stake input after a brief delay
    setTimeout(() => {
      const stakeInput = document.querySelector('input[formControlName="stake"]') as HTMLInputElement;
      if (stakeInput) {
        stakeInput.focus();
        stakeInput.select();
      }
    }, 300);
  }

  selectPrediction(prediction: 'home' | 'draw' | 'away'): void {
    this.selectedPrediction = prediction;
  }

  setStake(amount: number): void {
    this.betForm.patchValue({ stake: amount });
  }

  onSliderChange(event: any): void {
    this.betForm.patchValue({ stake: event.value });
  }

  isValidBet(): boolean {
    return this.betForm.valid && this.selectedPrediction !== null;
  }

  getSelectedOdds(): number {
    return this.data.match.odds[this.selectedPrediction];
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

  calculatePotentialWin(): number {
    const stake = this.betForm.get('stake')?.value || 0;
    const odds = this.getSelectedOdds();
    return stake * odds;
  }

  calculateNetProfit(): number {
    const stake = this.betForm.get('stake')?.value || 0;
    return this.calculatePotentialWin() - stake;
  }

  onPlaceBet(): void {
    if (this.isValidBet()) {
      const result: BetPlacementResult = {
        matchId: this.data.match.id,
        prediction: this.selectedPrediction,
        odds: this.getSelectedOdds(),
        stake: this.betForm.get('stake')?.value,
        potentialWin: this.calculatePotentialWin()
      };

      this.dialogRef.close(result);
    }
  }

  onCancel(): void {
    this.dialogRef.close(null);
  }
}