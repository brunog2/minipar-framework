import {
  ChangeDetectionStrategy,
  Component,
  HostListener,
  inject,
  signal,
  viewChild,
} from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatChipsModule } from '@angular/material/chips';
import { MatDividerModule } from '@angular/material/divider';
import { MatIconModule } from '@angular/material/icon';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatSlideToggleModule } from '@angular/material/slide-toggle';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatTooltipModule } from '@angular/material/tooltip';

import { APP_METADATA } from '../constants/app-metadata';
import { CodeTemplate } from '../constants/code-templates';
import { CodeEditorComponent } from '../editor/code-editor.component';
import { CodeTemplatePickerComponent } from '../editor/code-template-picker.component';
import { FeaturePanelComponent } from '../feature-panel/feature-panel.component';
import {
  ExecutionMode,
  ProcessResponse,
  TargetVariability,
} from '../models/process.models';
import { OutputPanelComponent } from '../output-panel/output-panel.component';
import { ServiceStatusComponent } from '../service-status/service-status.component';
import { CompilerApiService } from '../services/compiler-api.service';
import { ThemeService } from '../services/theme.service';
import { environment } from '../../environments/environment';

@Component({
  selector: 'app-compiler-workspace',
  imports: [
    MatToolbarModule,
    MatCardModule,
    MatButtonModule,
    MatIconModule,
    MatTooltipModule,
    MatSlideToggleModule,
    MatChipsModule,
    MatDividerModule,
    MatProgressSpinnerModule,
    MatSnackBarModule,
    CodeEditorComponent,
    CodeTemplatePickerComponent,
    FeaturePanelComponent,
    OutputPanelComponent,
    ServiceStatusComponent,
  ],
  templateUrl: './compiler-workspace.component.html',
  styleUrl: './compiler-workspace.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class CompilerWorkspaceComponent {
  private readonly editor = viewChild(CodeEditorComponent);
  protected readonly themeService = inject(ThemeService);

  protected readonly meta = APP_METADATA;
  protected readonly repositoryUrl = environment.repositoryUrl;

  protected readonly targetVariability = signal<TargetVariability>('INTERPRETER');
  protected readonly executionMode = signal<ExecutionMode>('LOCAL');
  protected readonly loading = signal(false);
  protected readonly result = signal<ProcessResponse | null>(null);
  protected readonly httpError = signal<string | null>(null);

  constructor(
    private readonly api: CompilerApiService,
    private readonly snackBar: MatSnackBar,
  ) {}

  @HostListener('document:keydown', ['$event'])
  onGlobalKeydown(event: KeyboardEvent): void {
    const isRun =
      event.key === 'F5' ||
      (event.key === 'Enter' && (event.ctrlKey || event.metaKey));

    if (!isRun) {
      return;
    }

    const target = event.target as HTMLElement | null;
    if (
      target &&
      (target.tagName === 'INPUT' ||
        target.tagName === 'TEXTAREA' ||
        target.isContentEditable)
    ) {
      return;
    }

    event.preventDefault();
    this.run();
  }

  run(): void {
    const editor = this.editor();
    const sourceCode = editor?.getCode() ?? '';

    this.loading.set(true);
    this.httpError.set(null);
    this.result.set(null);

    this.api
      .process({
        sourceCode,
        targetVariability: this.targetVariability(),
        executionMode: this.executionMode(),
      })
      .subscribe({
        next: (res) => {
          this.result.set(res);
          this.loading.set(false);
        },
        error: (err) => {
          this.httpError.set(
            err?.error?.message ?? err?.message ?? 'Falha ao contactar o gateway',
          );
          this.loading.set(false);
        },
      });
  }

  clearOutput(): void {
    this.result.set(null);
    this.httpError.set(null);
  }

  onTemplateSelected(template: CodeTemplate): void {
    this.editor()?.loadCode(template.code);
    this.clearOutput();

    this.snackBar.open(
      `Exemplo "${template.label}" carregado no editor. Pressione Executar para testar.`,
      'Fechar',
      { duration: 5000, horizontalPosition: 'center', verticalPosition: 'bottom' },
    );
  }

  onThemeToggle(checked: boolean): void {
    const desired: 'light' | 'dark' = checked ? 'dark' : 'light';
    if (this.themeService.theme() !== desired) {
      this.themeService.toggle();
    }
  }
}
