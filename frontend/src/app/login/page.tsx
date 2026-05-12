"use client";

import { signIn, useSession } from "next-auth/react";
import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { Sparkles } from "lucide-react";

export default function Login() {
  const { data: session, status } = useSession();
  const router = useRouter();

  useEffect(() => {
    if (status === "authenticated") {
      router.push("/");
    }
  }, [status, router]);

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-background overflow-hidden">
      
      {/* Background Ornaments */}
      <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] bg-blue-500/20 rounded-full blur-[120px] pointer-events-none" />
      <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-purple-500/20 rounded-full blur-[120px] pointer-events-none" />

      <div className="w-full max-w-md p-8 glass-card rounded-2xl relative z-10 mx-4 border border-white/10 shadow-2xl">
        <div className="text-center mb-8">
          <div className="w-12 h-12 bg-white/10 rounded-xl flex items-center justify-center mx-auto mb-4 border border-white/20 shadow-inner">
            <Sparkles className="text-blue-400" />
          </div>
          <h1 className="text-2xl font-bold tracking-tight text-white mb-2">Welcome to AutoHire</h1>
          <p className="text-sm text-zinc-400">Sign in to access your autonomous job application dashboard.</p>
        </div>

        <div className="space-y-3">
          <AuthButton provider="google" name="Google" icon="https://www.svgrepo.com/show/475656/google-color.svg" />
          <AuthButton provider="apple" name="Apple" icon="https://www.svgrepo.com/show/511330/apple-173.svg" invertIcon />
          <AuthButton provider="linkedin" name="LinkedIn" icon="https://www.svgrepo.com/show/448234/linkedin.svg" />
          <AuthButton provider="azure-ad" name="Outlook / Microsoft" icon="https://www.svgrepo.com/show/452236/microsoft.svg" />
          
          <div className="pt-4 mt-4 border-t border-white/10">
            <button 
              onClick={() => signIn("credentials", { username: "Developer Tester", callbackUrl: "/" })}
              className="w-full flex items-center justify-center gap-3 bg-blue-500/10 hover:bg-blue-500/20 text-blue-400 border border-blue-500/30 transition-colors py-3 px-4 rounded-xl text-sm font-medium group"
            >
              Developer MVP Login (Bypass OAuth)
            </button>
          </div>
        </div>

        <p className="text-center text-xs text-zinc-500 mt-8">
          By signing in, you agree to our Terms of Service and Privacy Policy.
        </p>
      </div>
    </div>
  );
}

function AuthButton({ provider, name, icon, invertIcon = false }: { provider: string, name: string, icon: string, invertIcon?: boolean }) {
  return (
    <button 
      onClick={() => signIn(provider)}
      className="w-full flex items-center justify-center gap-3 bg-white/5 hover:bg-white/10 border border-white/10 transition-colors py-3 px-4 rounded-xl text-sm font-medium text-white group"
    >
      <img src={icon} alt={name} className={`w-5 h-5 ${invertIcon ? 'invert' : ''}`} />
      Sign in with {name}
    </button>
  );
}
