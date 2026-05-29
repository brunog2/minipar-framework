import { ChangeDetectionStrategy, Component, input, output } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatRadioModule } from '@angular/material/radio';

import {
  ExecutionMode,
  TargetVariability,
} from '../models/process.models';

@Component({
  selector: 'app-feature-panel',
  imports: [
    MatCardModule,
    MatRadioModule,
    MatButtonModule,
    MatProgressSpinnerModule,
  ],
  templateUrl: './feature-panel.component.html',
  styleUrl: './feature-panel.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class FeaturePanelComponent {
  readonly targetVariability = input.required<TargetVariability>();
  readonly executionMode = input.required<ExecutionMode>();
  readonly loading = input(false);

  readonly targetChange = output<TargetVariability>();
  readonly executionChange = output<ExecutionMode>();
  readonly processClick = output<void>();

  readonly targets: { value: TargetVariability; label: string }[] = [
    { value: 'INTERPRETER', label: 'Interpretador' },
    { value: 'C', label: 'Compilador → C (gcc -O2)' },
    { value: 'CPP', label: 'Compilador → C++' },
    { value: 'RUST', label: 'Compilador → Rust' },
    { value: 'ASSEMBLY', label: 'Compilador → ARMv7' },
  ];

  readonly executions: { value: ExecutionMode; label: string }[] = [
    { value: 'LOCAL', label: 'Local' },
    {
      value: 'DISTRIBUTED_SOCKETS',
      label: 'Distribuído (sockets — 3 máquinas)',
    },
  ];

  onTargetChange(value: string): void {
    this.targetChange.emit(value as TargetVariability);
  }

  onExecutionChange(value: string): void {
    this.executionChange.emit(value as ExecutionMode);
  }
}
