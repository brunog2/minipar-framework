/** Microsserviços HTTP do pipeline — usado por GET /api/v1/services/health */
export interface ServiceDescriptor {
  name: string;
  port: number;
  envKey?: string;
  /** true = api-gateway (não faz probe HTTP externo) */
  self?: boolean;
}

export const SERVICE_REGISTRY: ServiceDescriptor[] = [
  { name: 'api-gateway', port: 3000, self: true },
  { name: 'ms-front-end', port: 3001, envKey: 'MS_FRONTEND_URL' },
  { name: 'ms-semantic', port: 3002, envKey: 'MS_SEMANTIC_URL' },
  { name: 'ms-interpreter', port: 3003, envKey: 'MS_INTERPRETER_URL' },
  { name: 'ms-codegen-c', port: 3004, envKey: 'MS_CODEGEN_C_URL' },
  { name: 'ms-codegen-rust', port: 3005, envKey: 'MS_CODEGEN_RUST_URL' },
  { name: 'ms-parallel-coord', port: 3006, envKey: 'MS_PARALLEL_COORD_URL' },
  { name: 'ms-codegen-arm', port: 3007, envKey: 'MS_CODEGEN_ARM_URL' },
  { name: 'ms-codegen-python', port: 3008, envKey: 'MS_CODEGEN_PYTHON_URL' },
];

export type ServiceHealthStatus = 'ok' | 'down' | 'unconfigured';

export interface ServiceHealthItem {
  name: string;
  port: number;
  status: ServiceHealthStatus;
}
