"use client";

import { useSession, signOut } from "next-auth/react";
import { UserCircle, ChevronRight, LogOut } from "lucide-react";
import Link from "next/link";

export default function UserProfileBadge() {
  const { data: session, status } = useSession();

  if (status === "loading") {
    return (
      <div className="glass-card rounded-xl p-4 flex items-center gap-3 animate-pulse">
        <div className="w-8 h-8 rounded-full bg-white/10"></div>
        <div className="flex-1 space-y-2">
          <div className="h-3 bg-white/10 rounded w-1/2"></div>
          <div className="h-2 bg-white/10 rounded w-1/3"></div>
        </div>
      </div>
    );
  }

  if (status === "authenticated" && session.user) {
    return (
      <div className="glass-card rounded-xl p-4 flex items-center gap-3 group relative cursor-pointer">
        {session.user.image ? (
          <img src={session.user.image} alt="Avatar" className="w-8 h-8 rounded-full border border-white/20" />
        ) : (
          <div className="w-8 h-8 rounded-full bg-blue-500/20 flex items-center justify-center border border-blue-500/30">
            <UserCircle size={16} className="text-blue-400" />
          </div>
        )}
        <div className="flex-1 overflow-hidden">
          <p className="text-sm font-medium truncate">{session.user.name}</p>
          <p className="text-xs text-muted-foreground truncate">{session.user.email}</p>
        </div>
        <button onClick={() => signOut()} className="text-zinc-500 hover:text-red-400 transition-colors" title="Sign Out">
          <LogOut size={16} />
        </button>
      </div>
    );
  }

  return (
    <Link href="/login">
      <div className="glass-card rounded-xl p-4 flex items-center gap-3 cursor-pointer group hover:border-blue-500/30 transition-colors">
        <div className="w-8 h-8 rounded-full bg-zinc-800 flex items-center justify-center border border-zinc-700">
          <UserCircle size={16} className="text-zinc-400" />
        </div>
        <div className="flex-1 overflow-hidden">
          <p className="text-sm font-medium truncate">Guest User</p>
          <p className="text-xs text-blue-400 truncate">Sign In &rarr;</p>
        </div>
      </div>
    </Link>
  );
}
