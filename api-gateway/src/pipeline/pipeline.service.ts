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

    if (executionMode === ExecutionMode.DISTRIBUTED_SOCKETS) {
      steps.push('ms-parallel-coord: coordinate (mock)');
    }

    let output: string;
    let generatedCode: string | undefined;

    switch (targetVariability) {
      case TargetVariability.INTERPRETER:
        steps.push('ms-interpreter: execute (mock)');
        output = `[Mock] Interpretador executou ${sourceCode.split('\n').length} linha(s).`;
        break;
      case TargetVariability.C:
      case TargetVariability.CPP:
        steps.push(`ms-codegen-c: generate target=${targetVariability} (mock)`);
        generatedCode =
          '/* Mock C/C++ */\nint main(void) { return 0; }\n';
        output = `[Mock] Código ${targetVariability} gerado (gcc -O2 pendente).`;
        break;
      case TargetVariability.RUST:
        steps.push('ms-codegen-rust: generate (mock)');
        generatedCode = 'fn main() {}\n';
        output = '[Mock] Código Rust gerado.';
        break;
      case TargetVariability.ASSEMBLY:
        steps.push('ms-codegen-arm: generate (mock)');
        generatedCode = '.text\n.global _start\n';
        output = '[Mock] Assembly ARMv7 gerado.';
        break;
      default:
        output = '[Mock] Processamento concluído.';
    }

    return {
      ast,
      symbolTable,
      output,
      generatedCode,
      pipelineSteps: steps,
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
      this.http.post<{ ast: unknown; errors?: string[] }>(
        `${frontendUrl}/parse`,
        { sourceCode },
      ),
    );
    steps.push('ms-front-end: parse');
    if (parseRes.data.errors?.length) {
      throw new Error(parseRes.data.errors.join('; '));
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
      throw new Error(semanticRes.data.errors.join('; '));
    }

    let backendOutput = '';
    let generatedCode: string | undefined;

    if (executionMode === ExecutionMode.DISTRIBUTED_SOCKETS) {
      const coordUrl = this.config.getOrThrow<string>('MS_PARALLEL_COORD_URL');
      await firstValueFrom(
        this.http.post(`${coordUrl}/coordinate`, {
          ast: semanticRes.data.ast,
          symbolTable: semanticRes.data.symbolTable,
          executionMode,
        }),
      );
      steps.push('ms-parallel-coord: coordinate');
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
        backendOutput = res.data.output;
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
        backendOutput = res.data.output;
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
        backendOutput = res.data.output;
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
        backendOutput = res.data.output;
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
    };
  }
}
