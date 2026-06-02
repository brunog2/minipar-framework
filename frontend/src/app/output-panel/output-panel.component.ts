import { JsonPipe } from '@angular/common';
import { ChangeDetectionStrategy, Component, computed, input } from '@angular/core';
import { MatCardModule } from '@angular/material/card';
import { MatChipsModule } from '@angular/material/chips';
import { MatIconModule } from '@angular/material/icon';
import { MatListModule } from '@angular/material/list';
import { MatTabsModule } from '@angular/material/tabs';

import { ProcessResponse } from '../models/process.models';

@Component({
  selector: 'app-output-panel',
  imports: [
    JsonPipe,
    MatCardModule,
    MatChipsModule,
    MatIconModule,
    MatListModule,
    MatTabsModule,
  ],
  templateUrl: './output-panel.component.html',
  styleUrl: './output-panel.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class OutputPanelComponent {
  readonly result = input<ProcessResponse | null>(null);
  readonly errorMessage = input<string | null>(null);

  protected readonly status = computed(() => this.resolveStatus());

  private resolveStatus(): {
    label: string;
    icon: string;
    tone: 'success' | 'error' | 'idle';
  } {
    const err = this.errorMessage();
    if (err) {
      return {
        label: this.errorKind(err),
        icon: 'error_outline',
        tone: 'error',
      };
    }

    const r = this.result();
    if (!r) {
      return { label: 'Pronto', icon: 'terminal', tone: 'idle' };
    }
    if (!r.success) {
      return {
        label: this.errorKind(r.error ?? 'Erro'),
        icon: 'error_outline',
        tone: 'error',
      };
    }
    return { label: 'Compilação OK', icon: 'check_circle', tone: 'success' };
  }

  private errorKind(message: string): string {
    if (message.includes('Parser error') || message.includes('Lexer error')) {
      return 'Erro sintático';
    }
    if (message.includes('Semantic error')) {
      return 'Erro semântico';
    }
    return 'Erro';
  }

  protected displayError(): string | null {
    return this.errorMessage() ?? this.result()?.error ?? null;
  }
}
