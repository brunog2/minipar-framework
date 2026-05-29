import { JsonPipe } from '@angular/common';
import { ChangeDetectionStrategy, Component, input } from '@angular/core';
import { MatCardModule } from '@angular/material/card';
import { MatListModule } from '@angular/material/list';

import { ProcessResponse } from '../models/process.models';

@Component({
  selector: 'app-output-panel',
  imports: [JsonPipe, MatCardModule, MatListModule],
  templateUrl: './output-panel.component.html',
  styleUrl: './output-panel.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class OutputPanelComponent {
  readonly result = input<ProcessResponse | null>(null);
  readonly errorMessage = input<string | null>(null);
}
