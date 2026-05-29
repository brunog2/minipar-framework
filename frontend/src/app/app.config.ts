import { provideHttpClient } from '@angular/common/http';
import {
  ApplicationConfig,
  importProvidersFrom,
  provideBrowserGlobalErrorListeners,
} from '@angular/core';
import { provideRouter } from '@angular/router';
import { provideAnimationsAsync } from '@angular/platform-browser/animations/async';
import {
  MonacoEditorModule,
  NgxMonacoEditorConfig,
} from 'ngx-monaco-editor-v2';

import { registerMiniparLanguage } from './editor/minipar-monaco.language';
import { routes } from './app.routes';

const monacoConfig: NgxMonacoEditorConfig = {
  // ngx-monaco-editor-v2 resolves "assets" → ./assets/monaco/min/vs (where loader.js lives)
  baseUrl: 'assets',
  defaultOptions: {
    theme: 'vs-dark',
    language: 'minipar',
    scrollBeyondLastLine: false,
    automaticLayout: true,
    minimap: { enabled: false },
    fontSize: 14,
    fontFamily: "'JetBrains Mono', 'Fira Code', monospace",
  },
  onMonacoLoad: () => registerMiniparLanguage(),
};

export const appConfig: ApplicationConfig = {
  providers: [
    provideBrowserGlobalErrorListeners(),
    provideRouter(routes),
    provideHttpClient(),
    provideAnimationsAsync(),
    importProvidersFrom(MonacoEditorModule.forRoot(monacoConfig)),
  ],
};
