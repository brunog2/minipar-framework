import { HttpModule } from '@nestjs/axios';
import { Module } from '@nestjs/common';
import { HistoryModule } from '../history/history.module';
import { PipelineModule } from '../pipeline/pipeline.module';
import { ProcessController } from './process.controller';
import { ProcessService } from './process.service';
import { ServicesHealthService } from './services-health.service';

@Module({
  imports: [
    PipelineModule,
    HistoryModule,
    HttpModule.register({ timeout: 5000 }),
  ],
  controllers: [ProcessController],
  providers: [ProcessService, ServicesHealthService],
})
export class ProcessModule {}
