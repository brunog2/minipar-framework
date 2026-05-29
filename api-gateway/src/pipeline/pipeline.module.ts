import { HttpModule } from '@nestjs/axios';
import { Module } from '@nestjs/common';
import { PipelineService } from './pipeline.service';

@Module({
  imports: [HttpModule.register({ timeout: 120000 })],
  providers: [PipelineService],
  exports: [PipelineService],
})
export class PipelineModule {}
