import { Injectable } from '@nestjs/common';
import { HistoryService } from '../history/history.service';
import { PipelineService } from '../pipeline/pipeline.service';
import { ProcessRequestDto } from './dto/process-request.dto';

@Injectable()
export class ProcessService {
  constructor(
    private readonly pipeline: PipelineService,
    private readonly history: HistoryService,
  ) {}

  async process(dto: ProcessRequestDto) {
    const record = await this.history.createRunning(
      dto.sourceCode,
      dto.targetVariability,
      dto.executionMode,
    );

    try {
      const result = await this.pipeline.run(
        dto.sourceCode,
        dto.targetVariability,
        dto.executionMode,
      );

      const outputPayload = JSON.stringify(
        {
          message: result.output,
          pipelineSteps: result.pipelineSteps,
          generatedCode: result.generatedCode,
        },
        null,
        2,
      );

      await this.history.markSuccess(record.id, outputPayload);

      return {
        success: true,
        historyId: record.id,
        targetVariability: dto.targetVariability,
        executionMode: dto.executionMode,
        output: result.output,
        ast: result.ast,
        symbolTable: result.symbolTable,
        generatedCode: result.generatedCode,
        pipelineSteps: result.pipelineSteps,
      };
    } catch (err: unknown) {
      const message =
        err instanceof Error ? err.message : 'Erro desconhecido no pipeline';
      await this.history.markError(record.id, message);
      return {
        success: false,
        historyId: record.id,
        error: message,
      };
    }
  }
}
