import { Body, Controller, Post } from '@nestjs/common';
import { ProcessRequestDto } from './dto/process-request.dto';
import { ProcessService } from './process.service';

@Controller('api/v1')
export class ProcessController {
  constructor(private readonly processService: ProcessService) {}

  @Post('process')
  process(@Body() dto: ProcessRequestDto) {
    return this.processService.process(dto);
  }
}
