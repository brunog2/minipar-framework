import { HttpClient } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';
import { ProcessRequest, ProcessResponse } from '../models/process.models';

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
}
