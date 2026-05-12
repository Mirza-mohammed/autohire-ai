"use client";

import { useState } from "react";
import { Plus, Play, Sparkles, CheckCircle2, Clock, XCircle, ChevronRight, Briefcase } from "lucide-react";

export default function Dashboard() {
  const [url, setUrl] = useState("");
  const [isProcessing, setIsProcessing] = useState(false);

  const handleTailor = (e: React.FormEvent) => {
    e.preventDefault();
    if (!url) return;
    setIsProcessing(true);
    // Simulate API call delay
    setTimeout(() => {
      setIsProcessing(false);
      setUrl("");
      alert("Application tailored and added to Kanban board!");
    }, 2000);
  };

  return (
    <div className="flex-1 p-8 overflow-y-auto">
      
      {/* Header */}
      <header className="mb-10">
        <h2 className="text-3xl font-bold text-white tracking-tight">Welcome back</h2>
        <p className="text-muted-foreground mt-1">Here is the status of your autonomous job applications.</p>
      </header>

      {/* Quick Action: New Application */}
      <div className="glass-card rounded-2xl p-6 mb-10 relative overflow-hidden group">
        <div className="absolute top-0 right-0 p-8 opacity-10 transform translate-x-4 -translate-y-4 group-hover:scale-110 transition-transform duration-700 pointer-events-none">
          <Sparkles size={120} className="text-blue-400" />
        </div>
        
        <h3 className="text-xl font-semibold mb-2 flex items-center gap-2">
          <Play size={20} className="text-blue-400" fill="currentColor" />
          Trigger Auto-Tailor
        </h3>
        <p className="text-sm text-zinc-400 mb-5 max-w-2xl">Paste a Job URL or raw job description here. Our AI agents will instantly parse requirements, tailor your master resume, and draft a cover letter.</p>
        
        <form onSubmit={handleTailor} className="flex gap-3 relative z-10 max-w-3xl">
          <input 
            type="text" 
            placeholder="https://linkedin.com/jobs/view/..." 
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            className="flex-1 bg-black/40 border border-white/10 rounded-lg px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/50 focus:border-blue-500/50 transition-all placeholder:text-zinc-600"
          />
          <button 
            type="submit"
            disabled={isProcessing}
            className="bg-white text-black font-semibold px-6 py-3 rounded-lg flex items-center gap-2 hover:bg-gray-200 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isProcessing ? (
              <span className="flex items-center gap-2">
                <svg className="animate-spin h-4 w-4 text-black" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle><path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
                Processing...
              </span>
            ) : (
              <>
                <Sparkles size={16} />
                Tailor & Apply
              </>
            )}
          </button>
        </form>
      </div>

      {/* Kanban Board Mockup */}
      <div>
        <div className="flex items-center justify-between mb-6">
          <h3 className="text-xl font-semibold">Active Applications</h3>
          <button className="text-sm text-blue-400 hover:text-blue-300 font-medium flex items-center gap-1 transition-colors">
            View All <ChevronRight size={16} />
          </button>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          
          {/* Column 1: Ready for Review */}
          <div className="bg-black/20 border border-white/5 rounded-xl p-4 flex flex-col gap-4">
            <div className="flex items-center justify-between px-2">
              <h4 className="text-sm font-medium text-amber-400 flex items-center gap-2">
                <Clock size={16} /> Ready for Review
              </h4>
              <span className="bg-amber-400/10 text-amber-400 text-xs py-0.5 px-2 rounded-full">2</span>
            </div>
            
            <KanbanCard company="Google" role="Senior AI Engineer" match={94} time="10m ago" />
            <KanbanCard company="Stripe" role="Backend Developer" match={88} time="1h ago" />
          </div>

          {/* Column 2: Applied */}
          <div className="bg-black/20 border border-white/5 rounded-xl p-4 flex flex-col gap-4">
            <div className="flex items-center justify-between px-2">
              <h4 className="text-sm font-medium text-blue-400 flex items-center gap-2">
                <CheckCircle2 size={16} /> Auto-Applied
              </h4>
              <span className="bg-blue-400/10 text-blue-400 text-xs py-0.5 px-2 rounded-full">1</span>
            </div>
            
            <KanbanCard company="Netflix" role="Platform Engineer" match={91} time="Yesterday" applied />
          </div>

          {/* Column 3: Rejected / Closed */}
          <div className="bg-black/20 border border-white/5 rounded-xl p-4 flex flex-col gap-4 opacity-70">
            <div className="flex items-center justify-between px-2">
              <h4 className="text-sm font-medium text-zinc-500 flex items-center gap-2">
                <XCircle size={16} /> Closed
              </h4>
              <span className="bg-zinc-800 text-zinc-400 text-xs py-0.5 px-2 rounded-full">1</span>
            </div>
            
            <KanbanCard company="Meta" role="Software Engineer" match={76} time="Last Week" rejected />
          </div>

        </div>
      </div>

    </div>
  );
}

function KanbanCard({ company, role, match, time, applied, rejected }: any) {
  return (
    <div className="glass-card p-4 rounded-lg cursor-pointer">
      <div className="flex justify-between items-start mb-3">
        <div className="w-10 h-10 rounded-md bg-white/5 border border-white/10 flex items-center justify-center">
          <Briefcase size={20} className="text-zinc-400" />
        </div>
        {match && (
          <div className="bg-green-500/10 border border-green-500/20 text-green-400 text-xs font-semibold px-2 py-1 rounded-md flex items-center gap-1">
            {match}% Match
          </div>
        )}
      </div>
      <h5 className="font-semibold text-white text-base truncate">{role}</h5>
      <p className="text-sm text-zinc-400 mb-4">{company}</p>
      
      <div className="flex items-center justify-between text-xs text-zinc-500 pt-3 border-t border-white/5">
        <span>{time}</span>
        {applied && <span className="text-blue-400 font-medium">Application Sent</span>}
        {rejected && <span className="text-red-400 font-medium">Rejected</span>}
        {!applied && !rejected && <span className="text-amber-400 font-medium hover:text-amber-300">Review & Apply &rarr;</span>}
      </div>
    </div>
  );
}
