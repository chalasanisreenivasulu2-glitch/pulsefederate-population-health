'use client';

import { useState } from 'react';
import { startTraining, getAuditLog, TrainResponse, TrainRequest } from '@/lib/api';
import ModelMetrics from '@/components/ModelMetrics';
import RiskHeatmap from '@/components/RiskHeatmap';
import AuditTrail from '@/components/AuditTrail';

export default function AdminPage() {
  const [result, setResult] = useState<TrainResponse | null>(null);
  const [audit, setAudit] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const [cfg, setCfg] = useState<TrainRequest>({
    rounds: 5,
    local_epochs: 2,
    dp_noise: 0.01,
    min_clients: 2,
  });

  async function handleTrain() {
    setLoading(true);
    setError(null);
    try {
      const r = await startTraining(cfg);
      setResult(r);
      const log = await getAuditLog();
      setAudit(log.events);
    } catch (e: any) {
      setError(e?.response?.data?.detail || e.message);
    } finally {
      setLoading(false);
    }
  }

  const lastRound = result?.rounds[result.rounds.length - 1];

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-end gap-4 rounded border border-slate-700 bg-slate-900 p-4">
        <label className="flex flex-col text-xs text-slate-400">
          Rounds
          <input
            type="number"
            className="mt-1 rounded bg-slate-800 px-2 py-1 text-slate-100"
            value={cfg.rounds}
            onChange={(e) => setCfg({ ...cfg, rounds: +e.target.value })}
          />
        </label>
        <label className="flex flex-col text-xs text-slate-400">
          Local Epochs
          <input
            type="number"
            className="mt-1 rounded bg-slate-800 px-2 py-1 text-slate-100"
            value={cfg.local_epochs}
            onChange={(e) => setCfg({ ...cfg, local_epochs: +e.target.value })}
          />
        </label>
        <label className="flex flex-col text-xs text-slate-400">
          DP Noise (sigma)
          <input
            type="number"
            step="0.01"
            className="mt-1 rounded bg-slate-800 px-2 py-1 text-slate-100"
            value={cfg.dp_noise}
            onChange={(e) => setCfg({ ...cfg, dp_noise: +e.target.value })}
          />
        </label>
        <button
          onClick={handleTrain}
          disabled={loading}
          className="rounded bg-emerald-600 px-4 py-2 text-white hover:bg-emerald-500 disabled:opacity-50"
        >
          {loading ? 'Training...' : 'Run Federated Training'}
        </button>
      </div>

      {error && (
        <div className="rounded border border-red-700 bg-red-950 p-3 text-sm text-red-300">
          {error}
        </div>
      )}

      {lastRound && (
        <div className="grid grid-cols-1 gap-4 md:grid-cols-3">
          <StatCard label="Final Accuracy" value={`${(lastRound.accuracy * 100).toFixed(1)}%`} />
          <StatCard label="Final Loss" value={lastRound.loss.toFixed(4)} />
          <StatCard label="Fairness Score" value={lastRound.fairness.toFixed(3)} />
        </div>
      )}

      {result && (
        <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
          <ModelMetrics rounds={result.rounds} />
          {lastRound && <RiskHeatmap clients={lastRound.clients} />}
        </div>
      )}

      <AuditTrail events={audit} />
    </div>
  );
}

function StatCard({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded border border-slate-700 bg-slate-900 p-4">
      <div className="text-xs uppercase tracking-wide text-slate-500">{label}</div>
      <div className="mt-1 text-2xl font-semibold text-slate-100">{value}</div>
    </div>
  );
}