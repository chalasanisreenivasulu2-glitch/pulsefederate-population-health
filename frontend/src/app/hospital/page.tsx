'use client';

import { useEffect, useState } from 'react';
import { listSites } from '@/lib/api';

export default function HospitalPage() {
  const [sites, setSites] = useState<string[]>([]);
  const [err, setErr] = useState<string | null>(null);

  useEffect(() => {
    listSites()
      .then((r) => setSites(r.sites))
      .catch((e) => setErr(e.message));
  }, []);

  return (
    <div className="space-y-4">
      <h2 className="text-xl font-semibold">Hospital Node View</h2>
      <p className="text-sm text-slate-400">
        Each site below trains locally and only shares model updates with the aggregator.
      </p>
      {err && <div className="text-red-400">Error: {err}</div>}
      <div className="grid grid-cols-1 gap-3 md:grid-cols-2">
        {sites.map((s) => (
          <div key={s} className="rounded border border-slate-700 bg-slate-900 p-4">
            <div className="text-xs uppercase tracking-wide text-slate-500">Node</div>
            <div className="mt-1 font-mono text-slate-100">{s}</div>
            <div className="mt-2 text-xs text-emerald-400">Local data never leaves this node</div>
          </div>
        ))}
        {sites.length === 0 && !err && <div className="text-slate-500">Loading sites...</div>}
      </div>
    </div>
  );
}