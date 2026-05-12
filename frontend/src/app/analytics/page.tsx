"use client";

import { useEffect, useState } from "react";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, ScatterChart, Scatter, ZAxis } from "recharts";
import { Activity, Target, Zap } from "lucide-react";

export default function AnalyticsDashboard() {
  const [funnelData, setFunnelData] = useState([]);
  const [performanceData, setPerformanceData] = useState([]);

  useEffect(() => {
    // In production, these would fetch from the real backend endpoint.
    // fetch("http://localhost:8000/api/v1/analytics/funnel/USER_ID")
    setFunnelData([
      { name: "Scraped", value: 120 },
      { name: "Evaluated", value: 85 },
      { name: "Auto-Applied", value: 45 },
      { name: "Interviewing", value: 8 },
      { name: "Closed", value: 37 }
    ]);

    setPerformanceData([
      { score: 95, outcome: 1, company: "Google" },
      { score: 92, outcome: 1, company: "Stripe" },
      { score: 88, outcome: 0, company: "Meta" },
      { score: 85, outcome: 0, company: "Amazon" },
      { score: 98, outcome: 1, company: "OpenAI" },
      { score: 81, outcome: 0, company: "Netflix" },
    ]);
  }, []);

  return (
    <div className="flex-1 p-8 overflow-y-auto">
      <header className="mb-10">
        <h2 className="text-3xl font-bold text-white tracking-tight">Analytics & Insights</h2>
        <p className="text-muted-foreground mt-1">Track the performance of your autonomous agent.</p>
      </header>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-10">
        <KPICard icon={<Activity />} title="Total Applications" value="45" trend="+12 this week" />
        <KPICard icon={<Target />} title="Interview Rate" value="17.7%" trend="+2.1% from last month" />
        <KPICard icon={<Zap />} title="Avg AI Tailoring Score" value="91.5" trend="Consistent" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        
        {/* Funnel Chart */}
        <div className="glass-card p-6 rounded-2xl">
          <h3 className="text-xl font-semibold mb-6">Application Funnel</h3>
          <div className="h-80">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={funnelData} margin={{ top: 20, right: 30, left: 0, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
                <XAxis dataKey="name" stroke="#a1a1aa" />
                <YAxis stroke="#a1a1aa" />
                <Tooltip 
                  cursor={{fill: 'rgba(255,255,255,0.05)'}}
                  contentStyle={{ backgroundColor: '#18181b', borderColor: '#27272a', borderRadius: '8px' }}
                />
                <Bar dataKey="value" fill="#60a5fa" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Scatter Plot */}
        <div className="glass-card p-6 rounded-2xl">
          <h3 className="text-xl font-semibold mb-6">Tailoring Score vs. Interview Rate</h3>
          <p className="text-sm text-zinc-400 mb-4">Outcome: 1 = Interview, 0 = Rejected/Ghosted</p>
          <div className="h-72">
            <ResponsiveContainer width="100%" height="100%">
              <ScatterChart margin={{ top: 20, right: 30, left: 0, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
                <XAxis type="number" dataKey="score" name="AI Match Score" domain={['dataMin - 5', 100]} stroke="#a1a1aa" />
                <YAxis type="number" dataKey="outcome" name="Outcome" domain={[-0.5, 1.5]} stroke="#a1a1aa" ticks={[0, 1]} />
                <ZAxis type="category" dataKey="company" name="Company" />
                <Tooltip 
                  cursor={{strokeDasharray: '3 3'}}
                  contentStyle={{ backgroundColor: '#18181b', borderColor: '#27272a', borderRadius: '8px' }}
                />
                <Scatter name="Applications" data={performanceData} fill="#f472b6" />
              </ScatterChart>
            </ResponsiveContainer>
          </div>
        </div>

      </div>
    </div>
  );
}

function KPICard({ icon, title, value, trend }: any) {
  return (
    <div className="glass-card p-6 rounded-xl flex items-start justify-between">
      <div>
        <p className="text-sm font-medium text-zinc-400 mb-1">{title}</p>
        <h4 className="text-3xl font-bold text-white mb-2">{value}</h4>
        <p className="text-xs text-green-400">{trend}</p>
      </div>
      <div className="w-10 h-10 rounded-full bg-white/5 flex items-center justify-center text-blue-400">
        {icon}
      </div>
    </div>
  );
}
