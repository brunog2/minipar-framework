import {
  ChangeDetectionStrategy,
  Component,
  inject,
  input,
  OnInit,
  signal,
} from '@angular/core';
import { MatCardModule } from '@angular/material/card';
import { MatChipsModule } from '@angular/material/chips';

import { ServiceHealth } from '../models/process.models';
import { CompilerApiService } from '../services/compiler-api.service';
import { environment } from '../../environments/environment';

const DEFAULT_SERVICES: ServiceHealth[] = [
  { name: 'api-gateway', port: 3000, status: 'unknown' },
  { name: 'ms-front-end', port: 3001, status: 'unknown' },
  { name: 'ms-semantic', port: 3002, status: 'unknown' },
  { name: 'ms-interpreter', port: 3003, status: 'unknown' },
  { name: 'ms-codegen-c', port: 3004, status: 'unknown' },
  { name: 'ms-codegen-rust', port: 3005, status: 'unknown' },
  { name: 'ms-parallel-coord', port: 3006, status: 'unknown' },
  { name: 'ms-codegen-arm', port: 3007, status: 'unknown' },
  { name: 'ms-codegen-python', port: 3008, status: 'unknown' },
];

@Component({
  selector: 'app-service-status',
  imports: [MatCardModule, MatChipsModule],
  template: `
    <mat-card class="status-card">
      <mat-card-header>
        <mat-card-title>Microsserviços</mat-card-title>
      </mat-card-header>
      <mat-card-content>
        @for (svc of services(); track svc.name) {
          <mat-chip-set>
            <mat-chip [class.ok]="svc.status === 'ok'">
              {{ svc.name }} :{{ svc.port }} — {{ svc.status }}
            </mat-chip>
          </mat-chip-set>
        }
      </mat-card-content>
    </mat-card>
  `,
  styles: `
    .status-card { margin-top: 1rem; }
    mat-chip.ok { --mdc-chip-label-text-color: #2e7d32; }
  `,
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class ServiceStatusComponent implements OnInit {
  private readonly api = inject(CompilerApiService);
  readonly compact = input(false);
  readonly services = signal<ServiceHealth[]>(DEFAULT_SERVICES);
  readonly recommendation = signal<string | null>(null);

  ngOnInit(): void {
    this.api.getRecommendations().subscribe({
      next: (rec) => this.recommendation.set(rec.reason),
      error: () => this.recommendation.set(null),
    });
    this.probeGateway();
  }

  private probeGateway(): void {
    const gateway = environment.apiUrl.replace(/\/$/, '');
    fetch(`${gateway}/health`)
      .then((r) => (r.ok ? 'ok' : 'down'))
      .then((status) => {
        this.services.update((list) =>
          list.map((s) =>
            s.name === 'api-gateway' ? { ...s, status } : s,
          ),
        );
      })
      .catch(() => undefined);
  }
}
