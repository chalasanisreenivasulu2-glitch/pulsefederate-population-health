'use client';

import {
  LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid,
} from 'recharts';
import type { RoundResult } from '@/lib/api';

export default function ModelMetrics({ rounds }: { rounds: RoundResult[] }) {
  const data = rounds.map((r) => ({
    round: r.round,
    accuracy: parseFloat(r.accuracy.toFixed(3)),
    fairness: parseFloat(r.fairness.toFixed(3)),
  }));

  return (
    <div className="rounded border border-slate-700 bg-slate-900 p-4">
      <h3 className="mb-2 text-sm font-semibold text-slate-300">
        Accuracy & Fairness per Round
      </h3>
      <ResponsiveContainer width="100%" height={260}>
        <LineChart data={data}>
          <CartesianGrid stroke="#334155" strokeDasharray="3 3" />
          <XAxis dataKey="round" stroke="#94a3b8" />
          <YAxis domain={[0, 1]} stroke="#94a3b8" />
          <Tooltip contentStyle={{ background: '#1e293b', border: '1px solid #334155' }} />
          <Line type="monotone" dataKey="accuracy" stroke="#10b981" strokeWidth={2} dot={false} />
          <Line type="monotone" dataKey="fairness" stroke="#60a5fa" strokeWidth={2} dot={false} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}