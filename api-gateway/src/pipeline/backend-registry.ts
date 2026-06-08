// Backend registry — adicionar um novo backend = adicionar uma linha aqui.
// Nenhum outro arquivo precisa ser modificado para registrar um novo backend.

export interface BackendDescriptor {
  variability: string;
  envKey: string;        // chave no .env com a URL do MS
  endpoint: string;      // path do endpoint no MS (ex: '/execute', '/generate')
  mockLabel: string;     // rótulo exibido no modo mock/dev
  mockCode?: string;     // código stub emitido no modo mock (undefined = sem código)
}

export const BACKEND_REGISTRY: BackendDescriptor[] = [
  {
    variability: 'INTERPRETER',
    envKey:      'MS_INTERPRETER_URL',
    endpoint:    '/execute',
    mockLabel:   'Interpretador',
  },
  {
    variability: 'C',
    envKey:      'MS_CODEGEN_C_URL',
    endpoint:    '/generate',
    mockLabel:   'Codegen C',
    mockCode:    '/* Mock C — Fase 2 */\nint main(void) { return 0; }\n',
  },
  {
    variability: 'CPP',
    envKey:      'MS_CODEGEN_C_URL',
    endpoint:    '/generate',
    mockLabel:   'Codegen C++',
    mockCode:    '/* Mock C++ — Fase 2 */\nint main() { return 0; }\n',
  },
  {
    variability: 'RUST',
    envKey:      'MS_CODEGEN_RUST_URL',
    endpoint:    '/generate',
    mockLabel:   'Codegen Rust',
    mockCode:    'fn main() {}\n',
  },
  {
    variability: 'ASSEMBLY',
    envKey:      'MS_CODEGEN_ARM_URL',
    endpoint:    '/generate',
    mockLabel:   'Codegen ARM',
    mockCode:    '.text\n.global _start\n',
  },
  {
    variability: 'PYTHON',
    envKey:      'MS_CODEGEN_PYTHON_URL',
    endpoint:    '/generate',
    mockLabel:   'Codegen Python',
    mockCode:    '# Mock Python — extension demo\nprint("mock")\n',
  },
];
