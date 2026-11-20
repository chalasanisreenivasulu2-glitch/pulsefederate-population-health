import './globals.css';
import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'PulseFederate',
  description: 'Privacy-preserving community risk stratification',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <header className="border-b border-slate-700 p-4">
          <h1 className="text-xl font-semibold">PulseFederate</h1>
          <nav className="mt-2 flex gap-4 text-sm text-slate-400">
            <a href="/" className="hover:text-slate-100">Home</a>
            <a href="/admin" className="hover:text-slate-100">Admin</a>
            <a href="/hospital" className="hover:text-slate-100">Hospital Node</a>
          </nav>
        </header>
        <main className="p-6">{children}</main>
      </body>
    </html>
  );
}