"use client";

import { useEffect, useState, useRef } from "react";
import { Terminal } from "lucide-react";

export default function TerminalLog() {
  const [logs, setLogs] = useState<string[]>([]);
  const scrollRef = useRef<HTMLDivElement>(null);
  const wsRef = useRef<WebSocket | null>(null);

  useEffect(() => {
    // Connect to FastAPI WebSocket
    const connectWs = () => {
      // In production, this should point to the wss:// backend URL
      const ws = new WebSocket("ws://localhost:8000/api/v1/ws/logs");
      wsRef.current = ws;

      ws.onmessage = (event) => {
        setLogs((prev) => [...prev, event.data]);
      };

      ws.onclose = () => {
        setLogs((prev) => [...prev, "[!] WebSocket disconnected. Reconnecting in 5s..."]);
        setTimeout(connectWs, 5000);
      };

      ws.onerror = () => {
        ws.close();
      };
    };

    connectWs();

    // Cleanup
    return () => {
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, []);

  // Auto-scroll to bottom
  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [logs]);

  return (
    <div className="glass-card rounded-2xl p-6 mt-8 border border-white/5 shadow-2xl flex flex-col h-[400px]">
      <div className="flex items-center gap-3 mb-4 pb-4 border-b border-white/10">
        <div className="w-10 h-10 rounded-full bg-green-500/10 flex items-center justify-center border border-green-500/30">
          <Terminal size={20} className="text-green-400" />
        </div>
        <div>
          <h3 className="text-lg font-semibold text-white tracking-tight">Live Worker Feed</h3>
          <p className="text-sm text-zinc-400">Real-time Celery execution logs via Redis Pub/Sub</p>
        </div>
        <div className="ml-auto flex gap-2">
          <div className="w-3 h-3 rounded-full bg-red-500/80"></div>
          <div className="w-3 h-3 rounded-full bg-yellow-500/80"></div>
          <div className="w-3 h-3 rounded-full bg-green-500/80"></div>
        </div>
      </div>

      <div 
        ref={scrollRef}
        className="flex-1 bg-[#0d1117] rounded-xl p-4 overflow-y-auto font-mono text-sm leading-relaxed border border-white/5"
      >
        {logs.length === 0 ? (
          <div className="text-zinc-500 italic">Connecting to Redis broker...</div>
        ) : (
          logs.map((log, i) => {
            let colorClass = "text-green-400";
            if (log.includes("[!]")) colorClass = "text-red-400 font-bold";
            if (log.includes("[*]")) colorClass = "text-blue-400";
            if (log.includes("[+]")) colorClass = "text-purple-400 font-medium";
            
            return (
              <div key={i} className={`mb-1 ${colorClass}`}>
                <span className="text-zinc-600 mr-3">[{new Date().toLocaleTimeString()}]</span>
                {log}
              </div>
            );
          })
        )}
        {/* Blinking cursor effect */}
        <div className="animate-pulse w-2 h-4 bg-green-400 inline-block mt-2"></div>
      </div>
    </div>
  );
}
