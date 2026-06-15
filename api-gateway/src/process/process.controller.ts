import { Body, Controller, Get, Post } from '@nestjs/common';
import { BACKEND_REGISTRY } from '../pipeline/backend-registry';
import { ProcessRequestDto } from './dto/process-request.dto';
import { ProcessService } from './process.service';
import { ServicesHealthService } from './services-health.service';

@Controller('api/v1')
export class ProcessController {
  constructor(
    private readonly processService: ProcessService,
    private readonly servicesHealthService: ServicesHealthService,
  ) {}

  @Get('variants')
  variants() {
    return BACKEND_REGISTRY.map((b) => ({
      variability: b.variability,
      label: b.mockLabel,
      endpoint: b.endpoint,
    }));
  }

  @Get('recommendations')
  recommendations() {
    return this.processService.getRecommendations();
  }

  @Get('services/health')
  getServicesHealth() {
    return this.servicesHealthService.getAll();
  }

  @Post('process')
  process(@Body() dto: ProcessRequestDto) {
    return this.processService.process(dto);
  }
}
