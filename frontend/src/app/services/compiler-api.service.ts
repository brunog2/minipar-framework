import { HttpClient } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';
import {
  ProcessRequest,
  ProcessResponse,
  RecommendationResponse,
  VariantOption,
} from '../models/process.models';

@Injectable({ providedIn: 'root' })
export class CompilerApiService {
  private readonly http = inject(HttpClient);
  private readonly baseUrl = environment.apiUrl;

  process(request: ProcessRequest): Observable<ProcessResponse> {
    return this.http.post<ProcessResponse>(
      `${this.baseUrl}/api/v1/process`,
      request,
    );
  }

  getVariants(): Observable<VariantOption[]> {
    return this.http.get<VariantOption[]>(`${this.baseUrl}/api/v1/variants`);
  }

  getRecommendations(): Observable<RecommendationResponse> {
    return this.http.get<RecommendationResponse>(
      `${this.baseUrl}/api/v1/recommendations`,
    );
  }
}
