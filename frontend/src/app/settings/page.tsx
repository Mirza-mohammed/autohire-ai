"use client";

import { useState } from "react";
import { Save, ShieldAlert, Cpu, Globe } from "lucide-react";

export default function Settings() {
  const [maxApps, setMaxApps] = useState(15);
  const [minMatch, setMinMatch] = useState(80);

  return (
    <div className="flex-1 p-8 overflow-y-auto">
      <header className="mb-10 flex items-center justify-between">
        <div>
          <h2 className="text-3xl font-bold text-white tracking-tight">Configuration & Settings</h2>
          <p className="text-muted-foreground mt-1">Fine-tune the behavior of your autonomous agent.</p>
        </div>
        <button className="flex items-center gap-2 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg text-sm font-medium transition-colors shadow-[0_0_15px_rgba(37,99,235,0.5)]">
          <Save size={16} />
          Save Preferences
        </button>
      </header>

      <div className="max-w-3xl space-y-8">
        
        {/* Rate Limits */}
        <section className="glass-card p-6 rounded-2xl">
          <div className="flex items-center gap-3 mb-6">
            <div className="w-10 h-10 rounded-full bg-orange-500/20 flex items-center justify-center border border-orange-500/30">
              <ShieldAlert size={20} className="text-orange-400" />
            </div>
            <div>
              <h3 className="text-xl font-semibold">Rate Limits & Safety</h3>
              <p className="text-sm text-zinc-400">Prevent getting banned from Handshake and LinkedIn.</p>
            </div>
          </div>
          
          <div className="space-y-6">
            <div>
              <div className="flex justify-between mb-2">
                <label className="text-sm font-medium text-zinc-300">Max Applications Per Day</label>
                <span className="text-sm font-bold text-blue-400">{maxApps} jobs</span>
              </div>
              <input 
                type="range" 
                min="1" 
                max="50" 
                value={maxApps}
                onChange={(e) => setMaxApps(parseInt(e.target.value))}
                className="w-full accent-blue-500"
              />
              <p className="text-xs text-zinc-500 mt-2">Applying to more than 20 jobs per day can flag your account as a bot.</p>
            </div>
          </div>
        </section>

        {/* AI Behavior */}
        <section className="glass-card p-6 rounded-2xl">
          <div className="flex items-center gap-3 mb-6">
            <div className="w-10 h-10 rounded-full bg-purple-500/20 flex items-center justify-center border border-purple-500/30">
              <Cpu size={20} className="text-purple-400" />
            </div>
            <div>
              <h3 className="text-xl font-semibold">AI Evaluation Thresholds</h3>
              <p className="text-sm text-zinc-400">Control how strict the LangChain evaluation agent is.</p>
            </div>
          </div>
          
          <div className="space-y-6">
            <div>
              <div className="flex justify-between mb-2">
                <label className="text-sm font-medium text-zinc-300">Minimum Match Score Trigger</label>
                <span className="text-sm font-bold text-blue-400">{minMatch}% Match</span>
              </div>
              <input 
                type="range" 
                min="50" 
                max="100" 
                value={minMatch}
                onChange={(e) => setMinMatch(parseInt(e.target.value))}
                className="w-full accent-blue-500"
              />
              <p className="text-xs text-zinc-500 mt-2">The AI will only Auto-Apply if the parsed job description matches your Master Resume &gt;= {minMatch}%.</p>
            </div>
            
            <div className="flex items-center justify-between p-4 bg-black/20 border border-white/5 rounded-xl">
              <div>
                <p className="text-sm font-medium text-white">Enable Reinforcement Learning Loop</p>
                <p className="text-xs text-zinc-500">Allow the AI to dynamically change its tailoring prompts based on past rejections.</p>
              </div>
              <label className="relative inline-flex items-center cursor-pointer">
                <input type="checkbox" defaultChecked className="sr-only peer" />
                <div className="w-11 h-6 bg-zinc-700 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-500"></div>
              </label>
            </div>
          </div>
        </section>

        {/* Job Search Preferences */}
        <section className="glass-card p-6 rounded-2xl">
          <div className="flex items-center gap-3 mb-6">
            <div className="w-10 h-10 rounded-full bg-green-500/20 flex items-center justify-center border border-green-500/30">
              <Globe size={20} className="text-green-400" />
            </div>
            <div>
              <h3 className="text-xl font-semibold">Job Search Preferences</h3>
              <p className="text-sm text-zinc-400">Filters applied to the background Scraper worker.</p>
            </div>
          </div>
          
          <div className="grid grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium text-zinc-400 mb-1">Work Type</label>
              <select className="w-full bg-black/20 border border-white/10 rounded-lg px-4 py-2.5 text-white focus:outline-none focus:border-blue-500/50 appearance-none">
                <option>Remote Only</option>
                <option>Hybrid</option>
                <option>On-site</option>
                <option>Any</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-zinc-400 mb-1">Minimum Base Salary (USD)</label>
              <input type="number" defaultValue="120000" className="w-full bg-black/20 border border-white/10 rounded-lg px-4 py-2.5 text-white focus:outline-none focus:border-blue-500/50" />
            </div>
          </div>
        </section>

      </div>
    </div>
  );
}
