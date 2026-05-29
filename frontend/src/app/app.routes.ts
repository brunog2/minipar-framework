import { Routes } from '@angular/router';
import { CompilerWorkspaceComponent } from './workspace/compiler-workspace.component';

export const routes: Routes = [
  { path: '', component: CompilerWorkspaceComponent },
  { path: '**', redirectTo: '' },
];
