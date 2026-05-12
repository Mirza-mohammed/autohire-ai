"use client";

import { useState } from "react";
import { Search, Filter, ExternalLink, MoreHorizontal, CheckCircle2, Clock, XCircle } from "lucide-react";

export default function Applications() {
  const [search, setSearch] = useState("");

  // Mock data for MVP
  const applications = [
    { id: "1", company: "Google", title: "Senior AI Engineer", date: "Oct 24, 2023", status: "applied", score: 95 },
    { id: "2", company: "Meta", title: "Machine Learning Engineer", date: "Oct 22, 2023", status: "rejected", score: 88 },
    { id: "3", company: "Stripe", title: "Backend Engineer", date: "Oct 20, 2023", status: "interview", score: 92 },
    { id: "4", company: "Netflix", title: "Data Scientist", date: "Oct 19, 2023", status: "pending", score: 81 },
    { id: "5", company: "Amazon", title: "SDE II", date: "Oct 15, 2023", status: "applied", score: 85 },
  ];

  return (
    <div className="flex-1 p-8 overflow-y-auto">
      <header className="mb-8">
        <h2 className="text-3xl font-bold text-white tracking-tight">Application History</h2>
        <p className="text-muted-foreground mt-1">Review your historical auto-applies and their exact tailoring scores.</p>
      </header>

      {/* Toolbar */}
      <div className="flex items-center gap-4 mb-6">
        <div className="flex-1 relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-zinc-500" size={18} />
          <input 
            type="text" 
            placeholder="Search company or role..." 
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-full bg-white/5 border border-white/10 rounded-lg pl-10 pr-4 py-2 text-sm text-white focus:outline-none focus:border-blue-500/50"
          />
        </div>
        <button className="flex items-center gap-2 px-4 py-2 bg-white/5 hover:bg-white/10 border border-white/10 rounded-lg text-sm font-medium transition-colors">
          <Filter size={16} />
          Filter
        </button>
      </div>

      {/* Data Table */}
      <div className="glass-card rounded-2xl overflow-hidden border border-white/10">
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="border-b border-white/10 bg-white/[0.02]">
                <th className="px-6 py-4 text-xs font-semibold text-zinc-400 uppercase tracking-wider">Company</th>
                <th className="px-6 py-4 text-xs font-semibold text-zinc-400 uppercase tracking-wider">Role</th>
                <th className="px-6 py-4 text-xs font-semibold text-zinc-400 uppercase tracking-wider">Date Applied</th>
                <th className="px-6 py-4 text-xs font-semibold text-zinc-400 uppercase tracking-wider">AI Tailoring Score</th>
                <th className="px-6 py-4 text-xs font-semibold text-zinc-400 uppercase tracking-wider">Status</th>
                <th className="px-6 py-4 text-xs font-semibold text-zinc-400 uppercase tracking-wider text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-white/5">
              {applications.filter(app => app.company.toLowerCase().includes(search.toLowerCase()) || app.title.toLowerCase().includes(search.toLowerCase())).map((app) => (
                <tr key={app.id} className="hover:bg-white/[0.02] transition-colors">
                  <td className="px-6 py-4 font-medium text-white">{app.company}</td>
                  <td className="px-6 py-4 text-zinc-300">{app.title}</td>
                  <td className="px-6 py-4 text-sm text-zinc-400">{app.date}</td>
                  <td className="px-6 py-4">
                    <div className="flex items-center gap-2">
                      <div className="w-full bg-white/10 rounded-full h-1.5 max-w-[100px]">
                        <div className="bg-blue-400 h-1.5 rounded-full" style={{ width: `${app.score}%` }}></div>
                      </div>
                      <span className="text-xs font-medium text-zinc-300">{app.score}%</span>
                    </div>
                  </td>
                  <td className="px-6 py-4">
                    <StatusBadge status={app.status} />
                  </td>
                  <td className="px-6 py-4 text-right">
                    <button className="text-zinc-500 hover:text-white transition-colors p-1">
                      <MoreHorizontal size={18} />
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

function StatusBadge({ status }: { status: string }) {
  const styles: Record<string, string> = {
    applied: "bg-blue-500/10 text-blue-400 border-blue-500/20",
    interview: "bg-green-500/10 text-green-400 border-green-500/20",
    rejected: "bg-red-500/10 text-red-400 border-red-500/20",
    pending: "bg-yellow-500/10 text-yellow-400 border-yellow-500/20",
  };

  const icons: Record<string, React.ReactNode> = {
    applied: <CheckCircle2 size={12} />,
    interview: <Clock size={12} />,
    rejected: <XCircle size={12} />,
    pending: <Clock size={12} />,
  };

  return (
    <span className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium border ${styles[status]}`}>
      {icons[status]}
      {status.charAt(0).toUpperCase() + status.slice(1)}
    </span>
  );
}
