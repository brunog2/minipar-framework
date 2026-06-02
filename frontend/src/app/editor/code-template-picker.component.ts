import {
  ChangeDetectionStrategy,
  Component,
  input,
  output,
  signal,
} from '@angular/core';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatIconModule } from '@angular/material/icon';
import { MatSelectModule } from '@angular/material/select';

import {
  CODE_TEMPLATE_GROUPS,
  CodeTemplate,
} from '../constants/code-templates';

@Component({
  selector: 'app-code-template-picker',
  imports: [MatFormFieldModule, MatSelectModule, MatIconModule],
  templateUrl: './code-template-picker.component.html',
  styleUrl: './code-template-picker.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class CodeTemplatePickerComponent {
  readonly disabled = input(false);

  readonly templateSelected = output<CodeTemplate>();

  protected readonly groups = CODE_TEMPLATE_GROUPS;
  protected readonly selectedId = signal('');
  protected readonly activeTemplate = signal<CodeTemplate | null>(null);

  onSelectionChange(id: string): void {
    if (!id) {
      this.selectedId.set('');
      this.activeTemplate.set(null);
      return;
    }

    const template = this.groups
      .flatMap((g) => g.templates)
      .find((t) => t.id === id);

    if (!template) {
      return;
    }

    this.selectedId.set(id);
    this.activeTemplate.set(template);
    this.templateSelected.emit(template);
  }
}
