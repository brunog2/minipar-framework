import { Injectable, effect, signal } from '@angular/core';

export type AppTheme = 'light' | 'dark';

const STORAGE_KEY = 'minipar-theme';

@Injectable({ providedIn: 'root' })
export class ThemeService {
  readonly theme = signal<AppTheme>(this.readStoredTheme());

  constructor() {
    effect(() => {
      const theme = this.theme();
      const root = document.documentElement;
      root.classList.remove('theme-light', 'theme-dark');
      root.classList.add(`theme-${theme}`);
      root.style.colorScheme = theme;
      try {
        localStorage?.setItem(STORAGE_KEY, theme);
      } catch {
        // indisponível em alguns ambientes de teste (jsdom)
      }
    });
  }

  toggle(): void {
    this.theme.update((current) => (current === 'dark' ? 'light' : 'dark'));
  }

  isDark(): boolean {
    return this.theme() === 'dark';
  }

  monacoTheme(): 'vs-dark' | 'vs' {
    return this.isDark() ? 'vs-dark' : 'vs';
  }

  private readStoredTheme(): AppTheme {
    try {
      const stored = localStorage?.getItem(STORAGE_KEY);
      return stored === 'light' || stored === 'dark' ? stored : 'dark';
    } catch {
      return 'dark';
    }
  }
}
