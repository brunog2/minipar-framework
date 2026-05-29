import { Injectable } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { CompilationHistory } from './entities/compilation-history.entity';

@Injectable()
export class HistoryService {
  constructor(
    @InjectRepository(CompilationHistory)
    private readonly repo: Repository<CompilationHistory>,
  ) {}

  async createRunning(
    sourceCode: string,
    targetVariability: string,
    executionMode: string,
  ): Promise<CompilationHistory> {
    const record = this.repo.create({
      sourceCode,
      targetVariability,
      executionMode,
      status: 'RUNNING',
      output: null,
      error: null,
    });
    return this.repo.save(record);
  }

  async markSuccess(id: string, output: string): Promise<void> {
    await this.repo.update(id, { status: 'SUCCESS', output, error: null });
  }

  async markError(id: string, error: string): Promise<void> {
    await this.repo.update(id, { status: 'ERROR', error });
  }
}
