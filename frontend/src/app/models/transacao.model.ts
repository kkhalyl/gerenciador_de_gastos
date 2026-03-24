export interface Transacao {
  id?: string;
  data_transacao: string;
  descricao: string;
  valor: number;
  saldo_apos_transacao: number;
  banco: string;
  categoria?: string;
}