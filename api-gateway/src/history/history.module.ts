import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
import { CompilationHistory } from './entities/compilation-history.entity';
import { HistoryService } from './history.service';

@Module({
  imports: [TypeOrmModule.forFeature([CompilationHistory])],
  providers: [HistoryService],
  exports: [HistoryService],
})
export class HistoryModule {}
