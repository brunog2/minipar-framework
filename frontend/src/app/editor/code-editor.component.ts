import {
  ChangeDetectionStrategy,
  Component,
  effect,
  inject,
  input,
  output,
} from '@angular/core';
import { FormsModule } from '@angular/forms';
import { MonacoEditorModule } from 'ngx-monaco-editor-v2';
import type { editor } from 'monaco-editor';

import { ThemeService } from '../services/theme.service';

@Component({
  selector: 'app-code-editor',
  imports: [MonacoEditorModule, FormsModule],
  templateUrl: './code-editor.component.html',
  styleUrl: './code-editor.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class CodeEditorComponent {
  private readonly themeService = inject(ThemeService);

  readonly initialCode = input<string>('');
  readonly codeChange = output<string>();

  protected source = DEFAULT_SAMPLE;
  protected editorOptions: editor.IStandaloneEditorConstructionOptions = {
    theme: this.themeService.monacoTheme(),
    language: 'minipar',
  };

  private monacoEditor?: editor.IStandaloneCodeEditor;

  constructor() {
    effect(() => {
      const monacoTheme = this.themeService.monacoTheme();
      this.editorOptions = { ...this.editorOptions, theme: monacoTheme };
      this.monacoEditor?.updateOptions({ theme: monacoTheme });
    });

    effect(() => {
      const code = this.initialCode();
      if (!code) {
        return;
      }
      if (this.monacoEditor) {
        const current = this.monacoEditor.getValue();
        if (code !== current) {
          this.monacoEditor.setValue(code);
        }
      } else {
        this.source = code;
      }
    });
  }

  onEditorInit(editorInstance: editor.IStandaloneCodeEditor): void {
    this.monacoEditor = editorInstance;
    editorInstance.updateOptions({ theme: this.themeService.monacoTheme() });

    const initial = this.initialCode();
    if (initial) {
      editorInstance.setValue(initial);
    } else if (!editorInstance.getValue()) {
      editorInstance.setValue(DEFAULT_SAMPLE);
    }
    this.source = editorInstance.getValue();

    editorInstance.onDidChangeModelContent(() => {
      this.source = editorInstance.getValue();
      this.codeChange.emit(this.source);
    });
  }

  getCode(): string {
    return this.monacoEditor?.getValue() ?? this.source;
  }
}

const DEFAULT_SAMPLE = `# MiniPar 2026.1 — exemplo
class Hello {
  func greet() -> void {
    print("Olá, MiniPar!")
  }
}

var h: Hello = new Hello()
h.greet()
`;
