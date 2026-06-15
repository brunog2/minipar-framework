import {
  ChangeDetectionStrategy,
  Component,
  inject,
  input,
  OnInit,
  output,
  signal,
} from '@angular/core';
import { MatCardModule } from '@angular/material/card';
import { MatIconModule } from '@angular/material/icon';
import { MatRadioModule } from '@angular/material/radio';

import {
  ExecutionMode,
  TargetVariability,
  VariantOption,
} from '../models/process.models';
import { CompilerApiService } from '../services/compiler-api.service';

@Component({
  selector: 'app-feature-panel',
  imports: [MatCardModule, MatRadioModule, MatIconModule],
  templateUrl: './feature-panel.component.html',
  styleUrl: './feature-panel.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class FeaturePanelComponent implements OnInit {
  private readonly api = inject(CompilerApiService);

  readonly targetVariability = input.required<TargetVariability>();
  readonly executionMode = input.required<ExecutionMode>();

  readonly targetChange = output<TargetVariability>();
  readonly executionChange = output<ExecutionMode>();

  readonly targets = signal<{ value: TargetVariability; label: string }[]>([
    { value: 'INTERPRETER', label: 'Interpretador' },
    { value: 'C', label: 'Compilador → C (gcc -O2)' },
    { value: 'CPP', label: 'Compilador → C++' },
    { value: 'RUST', label: 'Compilador → Rust' },
    { value: 'ASSEMBLY', label: 'Compilador → ARMv7' },
    { value: 'PYTHON', label: 'Compilador → Python (extensão)' },
  ]);

  readonly executions: { value: ExecutionMode; label: string }[] = [
    { value: 'LOCAL', label: 'Local' },
    {
      value: 'DISTRIBUTED_SOCKETS',
      label: 'Distribuído (sockets — 3 máquinas)',
    },
  ];

  ngOnInit(): void {
    this.api.getVariants().subscribe({
      next: (variants: VariantOption[]) => {
        if (variants.length) {
          this.targets.set(
            variants.map((v) => ({
              value: v.variability as TargetVariability,
              label: v.label,
            })),
          );
        }
      },
      error: () => undefined,
    });
  }

  onTargetChange(value: string): void {
    this.targetChange.emit(value as TargetVariability);
  }

  onExecutionChange(value: string): void {
    this.executionChange.emit(value as ExecutionMode);
  }
}
