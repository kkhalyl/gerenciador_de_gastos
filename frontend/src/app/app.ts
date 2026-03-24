import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Api } from './services/api';
import { Transacao } from './models/transacao.model';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule],
  styleUrl: './app.scss',
  template: `
    <div class="min-h-screen bg-gray-50 p-8">
      <div class="max-w-7xl mx-auto">
        
        <header class="mb-8">
          <h1 class="text-3xl font-bold text-gray-900">Dashboard Financeiro</h1>
          <p class="text-gray-500">Seu assistente inteligente (Dados do Bradesco)</p>
        </header>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          
          <div class="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
            <h3 class="text-sm font-medium text-gray-500 mb-1">Entradas (Receitas)</h3>
            <p class="text-2xl font-bold text-green-600">{{ totalEntradas | currency:'BRL' }}</p>
          </div>
          
          <div class="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
            <h3 class="text-sm font-medium text-gray-500 mb-1">Saídas (Despesas)</h3>
            <p class="text-2xl font-bold text-red-500">{{ totalSaidas | currency:'BRL' }}</p>
          </div>
          
          <div class="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
            <h3 class="text-sm font-medium text-gray-500 mb-1">Fluxo do Período</h3>
            <p class="text-2xl font-bold" [ngClass]="saldoTotal >= 0 ? 'text-blue-600' : 'text-red-600'">
              {{ saldoTotal | currency:'BRL' }}
            </p>
          </div>

        </div>

        <div class="bg-white shadow-sm border border-gray-100 rounded-xl overflow-hidden">
          <div class="overflow-x-auto">
            <table class="w-full text-left border-collapse">
              <thead class="bg-gray-50 border-b border-gray-100">
                <tr>
                  <th class="px-6 py-4 text-sm font-semibold text-gray-700">Data</th>
                  <th class="px-6 py-4 text-sm font-semibold text-gray-700">Descrição</th>
                  <th class="px-6 py-4 text-sm font-semibold text-gray-700 text-right">Valor</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-gray-100">
                <tr *ngFor="let t of transacoes" class="hover:bg-gray-50 transition-colors">
                  <td class="px-6 py-4 text-sm text-gray-600">{{ t.data_transacao | date:'dd/MM/yyyy' }}</td>
                  <td class="px-6 py-4 text-sm font-medium text-gray-900 uppercase">{{ t.descricao }}</td>
                  <td class="px-6 py-4 text-sm text-right font-bold"
                      [ngClass]="t.valor < 0 ? 'text-red-500' : 'text-green-600'">
                    {{ t.valor | currency:'BRL' }}
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

      </div>
    </div>
  `
})
export class AppComponent implements OnInit {
  transacoes: Transacao[] = [];
  totalEntradas = 0;
  totalSaidas = 0;
  saldoTotal = 0;

  constructor(private api: Api) {}

  ngOnInit() {
    this.api.getTransacoes().subscribe({
      next: (res) => {
        console.log("CHEGOU DO BACKEND:", res);
        this.transacoes = res.dados || res.data || [];
        this.calcularResumo();
      },
      error: (err) => console.error('Erro ao buscar dados:', err)
    });
  }

  // Função que varre as transações e faz a matemática financeira básica
  calcularResumo() {
    this.totalEntradas = this.transacoes
      .filter(t => t.valor > 0)
      .reduce((acc, curr) => acc + curr.valor, 0);

    this.totalSaidas = this.transacoes
      .filter(t => t.valor < 0)
      .reduce((acc, curr) => acc + curr.valor, 0);

    this.saldoTotal = this.totalEntradas + this.totalSaidas;
  }
}