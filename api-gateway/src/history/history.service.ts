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

  async getRecommendations(): Promise<{
    suggestedVariability: string;
    suggestedMode: string;
    reason: string;
    totalRuns: number;
    errorRate: number;
  }> {
    const rows = await this.repo.find({
      order: { createdAt: 'DESC' },
      take: 100,
    });
    if (!rows.length) {
      return {
        suggestedVariability: 'INTERPRETER',
        suggestedMode: 'LOCAL',
        reason: 'Sem histórico — usar interpretador local para primeira execução.',
        totalRuns: 0,
        errorRate: 0,
      };
    }
    const counts = new Map<string, number>();
    let errors = 0;
    for (const row of rows) {
      if (row.status === 'ERROR') {
        errors += 1;
      }
      if (row.status === 'SUCCESS') {
        const key = `${row.targetVariability}|${row.executionMode}`;
        counts.set(key, (counts.get(key) ?? 0) + 1);
      }
    }
    let best = 'INTERPRETER|LOCAL';
    let bestCount = 0;
    for (const [key, count] of counts.entries()) {
      if (count > bestCount) {
        best = key;
        bestCount = count;
      }
    }
    const [suggestedVariability, suggestedMode] = best.split('|');
    const last = rows[0];
    const reason =
      last.status === 'ERROR'
        ? `Última execução falhou (${last.targetVariability}). Variante mais bem-sucedida: ${suggestedVariability}.`
        : `Com base em ${rows.length} execuções recentes, ${suggestedVariability} + ${suggestedMode} teve melhor taxa de sucesso.`;
    return {
      suggestedVariability,
      suggestedMode,
      reason,
      totalRuns: rows.length,
      errorRate: rows.length ? errors / rows.length : 0,
    };
  }
}
