import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export interface ClientMetrics {
  client_id: string;
  num_samples: number;
  accuracy: number;
  loss: number;
}

export interface RoundResult {
  round: number;
  accuracy: number;
  loss: number;
  fairness: number;
  clients: ClientMetrics[];
  timestamp: string;
}

export interface TrainResponse {
  final_accuracy: number;
  rounds: RoundResult[];
}

export interface TrainRequest {
  rounds?: number;
  local_epochs?: number;
  learning_rate?: number;
  dp_noise?: number;
  dp_clip?: number;
  min_clients?: number;
}

const api = axios.create({ baseURL: API_URL, timeout: 120_000 });

export async function startTraining(req: TrainRequest): Promise<TrainResponse> {
  const { data } = await api.post<TrainResponse>('/api/train', req);
  return data;
}

export async function listSites(): Promise<{ sites: string[]; data_dir: string }> {
  const { data } = await api.get('/api/sites');
  return data;
}

export async function getAuditLog(): Promise<{ events: any[] }> {
  const { data } = await api.get('/api/audit');
  return data;
}