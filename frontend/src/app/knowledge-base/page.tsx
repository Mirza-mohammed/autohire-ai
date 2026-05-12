"use client";

import { useState, useRef } from "react";
import { UserCircle, Save, Plus, Trash2, UploadCloud, Loader2 } from "lucide-react";

export default function KnowledgeBase() {
  const [skills, setSkills] = useState("Python, React, TypeScript, FastAPI, Playwright");
  const [experience, setExperience] = useState([
    { title: "Software Engineer", company: "Tech Innovators", dates: "2021 - Present", bullets: "Built robust web applications." }
  ]);
  
  const [profile, setProfile] = useState({
    firstName: "Mohammad",
    lastName: "Mirza",
    email: "mohammad@example.com"
  });

  const [isUploading, setIsUploading] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setIsUploading(true);
    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch("http://localhost:8000/api/resume/parse", {
        method: "POST",
        body: formData,
      });
      const data = await response.json();
      
      if (data.status === "success" && data.data) {
        const parsed = data.data;
        setProfile({
          firstName: parsed.first_name || profile.firstName,
          lastName: parsed.last_name || profile.lastName,
          email: parsed.email || profile.email
        });
        setSkills(parsed.skills?.join(", ") || "");
        
        // Map extracted experience to UI format
        if (parsed.experience && parsed.experience.length > 0) {
          const newExp = parsed.experience.map((exp: any) => ({
            title: exp.title || "",
            company: exp.company || "",
            dates: exp.dates || "",
            bullets: exp.bullets || ""
          }));
          setExperience(newExp);
        }
      }
    } catch (error) {
      console.error("Failed to parse resume:", error);
      alert("Failed to parse resume. Ensure the backend is running.");
    } finally {
      setIsUploading(false);
    }
  };

  const addExperience = () => {
    setExperience([...experience, { title: "", company: "", dates: "", bullets: "" }]);
  };

  const removeExperience = (index: number) => {
    setExperience(experience.filter((_, i) => i !== index));
  };

  return (
    <div className="flex-1 p-8 overflow-y-auto">
      <header className="mb-10 flex items-center justify-between">
        <div>
          <h2 className="text-3xl font-bold text-white tracking-tight">Knowledge Base</h2>
          <p className="text-muted-foreground mt-1">Manage your Master Resume for the AI tailoring engine.</p>
        </div>
        <button className="flex items-center gap-2 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg text-sm font-medium transition-colors shadow-[0_0_15px_rgba(37,99,235,0.5)]">
          <Save size={16} />
          Save Changes
        </button>
      </header>

      {/* Upload Zone */}
      <div className="mb-8 p-8 glass-card border border-dashed border-white/20 hover:border-blue-500/50 transition-colors rounded-2xl flex flex-col items-center justify-center text-center cursor-pointer group" onClick={() => fileInputRef.current?.click()}>
        <input 
          type="file" 
          ref={fileInputRef} 
          onChange={handleFileUpload} 
          accept=".pdf" 
          className="hidden" 
        />
        {isUploading ? (
          <>
            <Loader2 size={32} className="text-blue-400 animate-spin mb-3" />
            <h3 className="text-lg font-medium text-white">Extracting your history...</h3>
            <p className="text-sm text-zinc-400 mt-1">OpenAI is parsing your PDF. This takes about 10 seconds.</p>
          </>
        ) : (
          <>
            <div className="w-12 h-12 rounded-full bg-blue-500/10 flex items-center justify-center mb-3 group-hover:bg-blue-500/20 transition-colors">
              <UploadCloud size={24} className="text-blue-400" />
            </div>
            <h3 className="text-lg font-medium text-white">Upload Existing Resume (PDF)</h3>
            <p className="text-sm text-zinc-400 mt-1">Skip the typing. Let the AI extract your skills and experience instantly.</p>
          </>
        )}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Core Profile */}
        <div className="lg:col-span-1 space-y-6">
          <div className="glass-card p-6 rounded-2xl">
            <div className="flex items-center gap-3 mb-6">
              <div className="w-10 h-10 rounded-full bg-blue-500/20 flex items-center justify-center border border-blue-500/30">
                <UserCircle size={20} className="text-blue-400" />
              </div>
              <h3 className="text-xl font-semibold">Core Identity</h3>
            </div>
            
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-zinc-400 mb-1">First Name</label>
                <input type="text" value={profile.firstName} onChange={(e) => setProfile({...profile, firstName: e.target.value})} className="w-full bg-black/20 border border-white/10 rounded-lg px-4 py-2.5 text-white focus:outline-none focus:border-blue-500/50 focus:ring-1 focus:ring-blue-500/50 transition-all" />
              </div>
              <div>
                <label className="block text-sm font-medium text-zinc-400 mb-1">Last Name</label>
                <input type="text" value={profile.lastName} onChange={(e) => setProfile({...profile, lastName: e.target.value})} className="w-full bg-black/20 border border-white/10 rounded-lg px-4 py-2.5 text-white focus:outline-none focus:border-blue-500/50 focus:ring-1 focus:ring-blue-500/50 transition-all" />
              </div>
              <div>
                <label className="block text-sm font-medium text-zinc-400 mb-1">Primary Email</label>
                <input type="email" value={profile.email} onChange={(e) => setProfile({...profile, email: e.target.value})} className="w-full bg-black/20 border border-white/10 rounded-lg px-4 py-2.5 text-white focus:outline-none focus:border-blue-500/50 focus:ring-1 focus:ring-blue-500/50 transition-all" />
              </div>
              <div>
                <label className="block text-sm font-medium text-zinc-400 mb-1">LinkedIn URL</label>
                <input type="url" defaultValue="https://linkedin.com/in/mohammad" className="w-full bg-black/20 border border-white/10 rounded-lg px-4 py-2.5 text-white focus:outline-none focus:border-blue-500/50 focus:ring-1 focus:ring-blue-500/50 transition-all" />
              </div>
            </div>
          </div>

          <div className="glass-card p-6 rounded-2xl">
             <h3 className="text-xl font-semibold mb-4">Master Skills Box</h3>
             <p className="text-xs text-zinc-400 mb-4">A comma-separated list of every skill you possess. The AI will cherry-pick from here.</p>
             <textarea 
               value={skills}
               onChange={(e) => setSkills(e.target.value)}
               className="w-full h-32 bg-black/20 border border-white/10 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-blue-500/50 transition-all resize-none" 
             />
          </div>
        </div>

        {/* Work Experience */}
        <div className="lg:col-span-2">
          <div className="glass-card p-6 rounded-2xl h-full">
            <div className="flex items-center justify-between mb-6">
              <h3 className="text-xl font-semibold">Work Experience & Projects</h3>
              <button onClick={addExperience} className="flex items-center gap-2 px-3 py-1.5 bg-white/5 hover:bg-white/10 border border-white/10 rounded-lg text-xs font-medium text-white transition-colors">
                <Plus size={14} />
                Add Entry
              </button>
            </div>

            <div className="space-y-6">
              {experience.map((exp, index) => (
                <div key={index} className="p-5 border border-white/5 bg-white/[0.02] rounded-xl relative group">
                  <button onClick={() => removeExperience(index)} className="absolute top-4 right-4 text-zinc-500 hover:text-red-400 opacity-0 group-hover:opacity-100 transition-all">
                    <Trash2 size={16} />
                  </button>
                  <div className="grid grid-cols-2 gap-4 mb-4">
                    <div>
                      <label className="block text-xs font-medium text-zinc-500 mb-1">Job Title / Project Name</label>
                      <input type="text" value={exp.title} onChange={(e) => { const newExp = [...experience]; newExp[index].title = e.target.value; setExperience(newExp); }} className="w-full bg-black/20 border border-white/10 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-blue-500/50" />
                    </div>
                    <div>
                      <label className="block text-xs font-medium text-zinc-500 mb-1">Company / Institution</label>
                      <input type="text" value={exp.company} onChange={(e) => { const newExp = [...experience]; newExp[index].company = e.target.value; setExperience(newExp); }} className="w-full bg-black/20 border border-white/10 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-blue-500/50" />
                    </div>
                  </div>
                  <div>
                    <label className="block text-xs font-medium text-zinc-500 mb-1">Raw Bullet Points (The AI will rewrite these)</label>
                    <textarea value={exp.bullets} onChange={(e) => { const newExp = [...experience]; newExp[index].bullets = e.target.value; setExperience(newExp); }} className="w-full h-24 bg-black/20 border border-white/10 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-blue-500/50 resize-none" />
                  </div>
                </div>
              ))}
            </div>

          </div>
        </div>

      </div>
    </div>
  );
}
