'use client';

import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from 'recharts';
import type { ClientMetrics } from '@/lib/api';

export default function RiskHeatmap({ clients }: { clients: ClientMetrics[] }) {
  const data = clients.map((c) => ({
    name: c.client_id,
    risk: parseFloat((1 - c.accuracy).toFixed(3)),
  }));

  const colorFor = (risk: number) =>
    risk < 0.2 ? '#10b981' : risk < 0.35 ? '#f59e0b' : '#ef4444';

  return (
    <div className="rounded border border-slate-700 bg-slate-900 p-4">
      <h3 className="mb-2 text-sm font-semibold text-slate-300">
        Per-Site Risk (Higher = Worse)
      </h3>
      <ResponsiveContainer width="100%" height={240}>
        <BarChart data={data}>
          <XAxis dataKey="name" stroke="#94a3b8" />
          <YAxis stroke="#94a3b8" domain={[0, 1]} />
          <Tooltip
            contentStyle={{ background: '#1e293b', border: '1px solid #334155' }}
            formatter={(v: number) => [`${(v * 100).toFixed(1)}%`, 'Risk']}
          />
          <Bar dataKey="risk">
            {data.map((d, i) => (
              <Cell key={i} fill={colorFor(d.risk)} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}