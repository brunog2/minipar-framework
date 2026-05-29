export type TargetVariability =
  | 'INTERPRETER'
  | 'C'
  | 'CPP'
  | 'RUST'
  | 'ASSEMBLY';

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
  error?: string;
}
