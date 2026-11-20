export default function AuditTrail({ events }: { events: any[] }) {
  return (
    <div className="rounded border border-slate-700 bg-slate-900 p-4">
      <h3 className="mb-2 text-sm font-semibold text-slate-300">Audit Trail</h3>
      <ul className="space-y-1 text-xs text-slate-400">
        {events.length === 0 && <li>No events yet.</li>}
        {events.map((e, i) => (
          <li key={i} className="border-l-2 border-emerald-600 pl-2">
            <span className="text-slate-200">{e.event}</span>{' '}
            <span className="text-slate-500">— {e.time}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}