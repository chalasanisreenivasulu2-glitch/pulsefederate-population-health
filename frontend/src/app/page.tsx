export default function Home() {
  return (
    <div className="max-w-2xl space-y-4">
      <h2 className="text-2xl font-bold">Signals to Solutions</h2>
      <p className="text-slate-300">
        A federated learning platform for community risk stratification.
        Hospital nodes train locally; only model weights are shared — never raw data.
      </p>
      <ul className="list-disc space-y-1 pl-6 text-slate-400">
        <li>Differential-privacy trained models</li>
        <li>Weighted FedAvg aggregation</li>
        <li>Fairness tracking across sites</li>
        <li>Real-time admin dashboard</li>
      </ul>
      <div className="flex gap-3 pt-4">
        <a href="/admin" className="rounded bg-emerald-600 px-4 py-2 text-white hover:bg-emerald-500">
          Open Admin Dashboard
        </a>
        <a href="/hospital" className="rounded border border-slate-600 px-4 py-2 hover:bg-slate-800">
          Hospital Node View
        </a>
      </div>
    </div>
  );
}