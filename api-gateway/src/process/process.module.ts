import { Module } from '@nestjs/common';
import { HistoryModule } from '../history/history.module';
import { PipelineModule } from '../pipeline/pipeline.module';
import { ProcessController } from './process.controller';
import { ProcessService } from './process.service';

@Module({
  imports: [PipelineModule, HistoryModule],
  controllers: [ProcessController],
  providers: [ProcessService],
})
export class ProcessModule {}
