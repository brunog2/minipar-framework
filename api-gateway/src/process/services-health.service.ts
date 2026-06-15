import { HttpService } from '@nestjs/axios';
import { Injectable } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import { firstValueFrom } from 'rxjs';
import {
  SERVICE_REGISTRY,
  ServiceHealthItem,
  ServiceHealthStatus,
} from './service-registry';

const PROBE_TIMEOUT_MS = 4000;

@Injectable()
export class ServicesHealthService {
  constructor(
    private readonly config: ConfigService,
    private readonly http: HttpService,
  ) {}

  async getAll(): Promise<ServiceHealthItem[]> {
    const results = await Promise.all(
      SERVICE_REGISTRY.map((svc) => this.probe(svc.name, svc.port, svc.envKey, svc.self)),
    );
    return results;
  }

  private async probe(
    name: string,
    port: number,
    envKey?: string,
    self?: boolean,
  ): Promise<ServiceHealthItem> {
    if (self) {
      return { name, port, status: 'ok' };
    }
    if (!envKey) {
      return { name, port, status: 'unconfigured' };
    }
    const baseUrl = this.config.get<string>(envKey);
    if (!baseUrl) {
      return { name, port, status: 'unconfigured' };
    }
    const status = await this.fetchHealth(baseUrl);
    return { name, port, status };
  }

  private async fetchHealth(baseUrl: string): Promise<ServiceHealthStatus> {
    const url = `${baseUrl.replace(/\/$/, '')}/health`;
    try {
      const res = await firstValueFrom(
        this.http.get(url, { timeout: PROBE_TIMEOUT_MS, validateStatus: () => true }),
      );
      return res.status >= 200 && res.status < 300 ? 'ok' : 'down';
    } catch {
      return 'down';
    }
  }
}
