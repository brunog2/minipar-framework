import { HttpService } from '@nestjs/axios';
import { Injectable } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import { firstValueFrom } from 'rxjs';
import { ExecutionMode } from '../process/enums/execution-mode.enum';
import { TargetVariability } from '../process/enums/target-variability.enum';

export interface PipelineResult {
  ast: unknown;
  symbolTable: unknown;
  output: string;
  generatedCode?: string;
  pipelineSteps: string[];
  distributedResults?: Array<{
    role: string;
    data: string;
    machine?: string;
    error?: string;
  }>;
}

@Injectable()
export class PipelineService {
  constructor(
    private readonly http: HttpService,
    private readonly config: ConfigService,
  ) {}

  async run(
    sourceCode: string,
    targetVariability: TargetVariability,
    executionMode: ExecutionMode,
  ): Promise<PipelineResult> {
    const mode = this.config.get<string>('PIPELINE_MODE', 'mock');
    if (mode === 'mock') {
      return this.runMock(sourceCode, targetVariability, executionMode);
    }
    return this.runHttp(sourceCode, targetVariability, executionMode);
  }

  private formatErrors(errors: unknown[]): string {
    return errors
      .map((e) =>
        typeof e === 'string'
          ? e
          : e && typeof e === 'object' && 'message' in e
            ? String((e as { message: string }).message)
            : String(e),
      )
      .join('; ');
  }

  private runMockBackend(
    sourceCode: string,
    targetVariability: TargetVariability,
    executionMode: ExecutionMode,
    steps: string[],
  ): {
    output: string;
    generatedCode?: string;
    distributedResults?: Array<{
      role: string;
      data: string;
      machine?: string;
    }>;
  } {
    let distributedResults:
      | Array<{ role: string; data: string; machine?: string }>
      | undefined;

    if (executionMode === ExecutionMode.DISTRIBUTED_SOCKETS) {
      steps.push('ms-parallel-coord: coordinate (mock)');
      distributedResults = [
        {
          role: 'quicksort',
          machine: 'PC1',
          data: 'QuickSort: [64, 34, 25, 12, 22, 11, 90] -> [11, 12, 22, 25, 34, 64, 90]',
        },
        {
          role: 'matrix',
          machine: 'PC2',
          data: 'Matriz 2x2: [[19, 22], [43, 50]]',
        },
        {
          role: 'factorial',
          machine: 'PC3',
          data: 'Fatorial(10) = 3628800',
        },
      ];
    }

    let outputPrefix = '';
    if (distributedResults?.length) {
      outputPrefix =
        '=== Menu Coordenador — Paralelismo Real (3 Máquinas) ===\n' +
        distributedResults
          .map((r) => `[${r.machine ?? r.role}] ${r.data}`)
          .join('\n') +
        '\n\n';
    }

    let output: string;
    let generatedCode: string | undefined;

    switch (targetVariability) {
      case TargetVariability.INTERPRETER:
        steps.push('ms-interpreter: execute (mock)');
        output = `[Fase 1] Análise concluída. Interpretador pendente (Fase 2). ${sourceCode.split('\n').length} linha(s).`;
        break;
      case TargetVariability.C:
      case TargetVariability.CPP:
        steps.push(`ms-codegen-c: generate target=${targetVariability} (mock)`);
        generatedCode = '/* Mock C/C++ — Fase 2 */\nint main(void) { return 0; }\n';
        output = `[Fase 1] AST validada. Codegen ${targetVariability} pendente (Fase 2).`;
        break;
      case TargetVariability.RUST:
        steps.push('ms-codegen-rust: generate (mock)');
        generatedCode = 'fn main() {}\n';
        output = '[Fase 1] AST validada. Codegen Rust pendente (Fase 2).';
        break;
      case TargetVariability.ASSEMBLY:
        steps.push('ms-codegen-arm: generate (mock)');
        generatedCode = '.text\n.global _start\n';
        output = '[Fase 1] AST validada. Codegen ARM pendente (Fase 2).';
        break;
      default:
        output = '[Fase 1] Processamento front-end concluído.';
    }

    return { output: outputPrefix + output, generatedCode, distributedResults };
  }

  private runMock(
    sourceCode: string,
    targetVariability: TargetVariability,
    executionMode: ExecutionMode,
  ): PipelineResult {
    const ast = {
      type: 'Program',
      declarations: [
        {
          type: 'ClassDecl',
          name: 'MockProgram',
          extends: null,
          members: [],
        },
      ],
      _meta: { sourceLength: sourceCode.length, mode: 'mock' },
    };

    const symbolTable = {
      scopes: [{ name: 'global', symbols: [] }],
      _meta: { mode: 'mock' },
    };

    const steps = [
      'ms-front-end: parse (mock)',
      'ms-semantic: analyze (mock)',
    ];

    const backend = this.runMockBackend(
      sourceCode,
      targetVariability,
      executionMode,
      steps,
    );

    return {
      ast,
      symbolTable,
      output: backend.output,
      generatedCode: backend.generatedCode,
      pipelineSteps: steps,
      distributedResults: backend.distributedResults,
    };
  }

  private async runHttp(
    sourceCode: string,
    targetVariability: TargetVariability,
    executionMode: ExecutionMode,
  ): Promise<PipelineResult> {
    const steps: string[] = [];

    const frontendUrl = this.config.getOrThrow<string>('MS_FRONTEND_URL');
    const semanticUrl = this.config.getOrThrow<string>('MS_SEMANTIC_URL');

    const parseRes = await firstValueFrom(
      this.http.post<{ ast: unknown; errors?: unknown[] }>(
        `${frontendUrl}/parse`,
        { sourceCode },
      ),
    );
    steps.push('ms-front-end: parse');
    if (parseRes.data.errors?.length) {
      throw new Error(this.formatErrors(parseRes.data.errors));
    }
    if (!parseRes.data.ast) {
      throw new Error('Parser returned empty AST');
    }

    const semanticRes = await firstValueFrom(
      this.http.post<{
        ast: unknown;
        symbolTable: unknown;
        errors?: string[];
      }>(`${semanticUrl}/analyze`, { ast: parseRes.data.ast }),
    );
    steps.push('ms-semantic: analyze');
    if (semanticRes.data.errors?.length) {
      throw new Error(this.formatErrors(semanticRes.data.errors));
    }

    const backendMode = this.config.get<string>(
      'PIPELINE_BACKEND_MODE',
      'mock',
    );

    if (backendMode === 'mock') {
      const backend = this.runMockBackend(
        sourceCode,
        targetVariability,
        executionMode,
        steps,
      );
      return {
        ast: semanticRes.data.ast,
        symbolTable: semanticRes.data.symbolTable,
        output: backend.output,
        generatedCode: backend.generatedCode,
        pipelineSteps: steps,
      };
    }

    let backendOutput = '';
    let generatedCode: string | undefined;
    let distributedResults:
      | Array<{
          role: string;
          data: string;
          machine?: string;
          error?: string;
        }>
      | undefined;

    if (executionMode === ExecutionMode.DISTRIBUTED_SOCKETS) {
      const coordUrl = this.config.getOrThrow<string>('MS_PARALLEL_COORD_URL');
      const coordRes = await firstValueFrom(
        this.http.post<{
          output: string;
          results: Array<{
            role: string;
            data: string;
            machine?: string;
            error?: string;
          }>;
        }>(`${coordUrl}/coordinate`, {
          ast: semanticRes.data.ast,
          symbolTable: semanticRes.data.symbolTable,
          executionMode,
        }),
      );
      steps.push('ms-parallel-coord: coordinate');
      distributedResults = coordRes.data.results;
      backendOutput = coordRes.data.output + '\n';
    }

    const payload = {
      ast: semanticRes.data.ast,
      symbolTable: semanticRes.data.symbolTable,
      executionMode,
      target: targetVariability,
    };

    switch (targetVariability) {
      case TargetVariability.INTERPRETER: {
        const url = this.config.getOrThrow<string>('MS_INTERPRETER_URL');
        const res = await firstValueFrom(
          this.http.post<{ output: string }>(`${url}/execute`, payload),
        );
        steps.push('ms-interpreter: execute');
        backendOutput += res.data.output;
        break;
      }
      case TargetVariability.C:
      case TargetVariability.CPP: {
        const url = this.config.getOrThrow<string>('MS_CODEGEN_C_URL');
        const res = await firstValueFrom(
          this.http.post<{ output: string; code?: string }>(
            `${url}/generate`,
            { ...payload, target: targetVariability },
          ),
        );
        steps.push(`ms-codegen-c: generate (${targetVariability})`);
        backendOutput += res.data.output;
        generatedCode = res.data.code;
        break;
      }
      case TargetVariability.RUST: {
        const url = this.config.getOrThrow<string>('MS_CODEGEN_RUST_URL');
        const res = await firstValueFrom(
          this.http.post<{ output: string; code?: string }>(
            `${url}/generate`,
            payload,
          ),
        );
        steps.push('ms-codegen-rust: generate');
        backendOutput += res.data.output;
        generatedCode = res.data.code;
        break;
      }
      case TargetVariability.ASSEMBLY: {
        const url = this.config.getOrThrow<string>('MS_CODEGEN_ARM_URL');
        const res = await firstValueFrom(
          this.http.post<{ output: string; code?: string }>(
            `${url}/generate`,
            payload,
          ),
        );
        steps.push('ms-codegen-arm: generate');
        backendOutput += res.data.output;
        generatedCode = res.data.code;
        break;
      }
      default:
        backendOutput = 'Backend não configurado.';
    }

    return {
      ast: semanticRes.data.ast,
      symbolTable: semanticRes.data.symbolTable,
      output: backendOutput,
      generatedCode,
      pipelineSteps: steps,
      distributedResults,
    };
  }
}
