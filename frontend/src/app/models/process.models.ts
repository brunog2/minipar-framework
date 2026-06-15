export type TargetVariability =
  | 'INTERPRETER'
  | 'C'
  | 'CPP'
  | 'RUST'
  | 'ASSEMBLY'
  | 'PYTHON';

export type ExecutionMode = 'LOCAL' | 'DISTRIBUTED_SOCKETS';

export interface ProcessRequest {
  sourceCode: string;
  targetVariability: TargetVariability;
  executionMode: ExecutionMode;
}

export interface ProcessResponse {
  success: boolean;
  historyId?: string;
  targetVariability?: TargetVariability;
  executionMode?: ExecutionMode;
  output?: string;
  ast?: unknown;
  symbolTable?: unknown;
  generatedCode?: string;
  pipelineSteps?: string[];
  distributedResults?: DistributedWorkerResult[];
  error?: string;
}

export interface VariantOption {
  variability: string;
  label: string;
  endpoint: string;
}

export interface RecommendationResponse {
  suggestedVariability: string;
  suggestedMode: string;
  reason: string;
  totalRuns: number;
  errorRate: number;
}

export type ServiceHealthStatus = 'ok' | 'down' | 'unconfigured' | 'unknown';

export interface ServiceHealth {
  name: string;
  port: number;
  status: ServiceHealthStatus;
}

export interface DistributedWorkerResult {
  role: string;
  data: string;
  machine?: string;
  error?: string;
}
