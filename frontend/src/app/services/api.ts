import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs'
import { Transacao } from '../models/transacao.model';

@Injectable({
  providedIn: 'root',
})
export class Api {
  private apiUrl = 'https://turbo-potato-764g9xqw96vcrvr6-8000.app.github.dev/'

  constructor(private http: HttpClient) {}

  getTransacoes(): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}api/transacoes`);
  }

  uploadExtrato(banco: string, arquivo: File): Observable<any> {
    const formData = new FormData();
    formData.append('file', arquivo);
    return this.http.post(`${this.apiUrl}api/upload-extrato/${banco}`, formData);
  }
}
