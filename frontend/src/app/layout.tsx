import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { Home, Briefcase, UserCircle, Settings, ChevronRight, BarChart3 } from "lucide-react";
import Link from "next/link";
import SessionWrapper from "@/components/SessionWrapper";
import UserProfileBadge from "@/components/UserProfileBadge";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "AutoHire AI",
  description: "Autonomous Job Application Platform",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <body className={`${inter.className} bg-background text-foreground min-h-screen flex antialiased`}>
        <SessionWrapper>
        {/* Sidebar */}
        <aside className="w-64 glass border-r border-white/5 flex flex-col hidden md:flex h-screen sticky top-0">
          <div className="p-6">
            <h1 className="text-2xl font-bold tracking-tight text-gradient">AutoHire AI</h1>
            <p className="text-xs text-muted-foreground mt-1 tracking-wider uppercase">Autonomous Platform</p>
          </div>
          
          <nav className="flex-1 px-4 space-y-2 mt-4">
            <NavItem href="/" icon={<Home size={18} />} label="Dashboard" />
            <NavItem href="/analytics" icon={<BarChart3 size={18} />} label="Analytics" />
            <NavItem href="#" icon={<Briefcase size={18} />} label="Applications" />
            <NavItem href="#" icon={<UserCircle size={18} />} label="Knowledge Base" />
            <NavItem href="#" icon={<Settings size={18} />} label="Settings" />
          </nav>

          <div className="p-4 mt-auto">
            <UserProfileBadge />
          </div>
        </aside>

        {/* Main Content */}
        <main className="flex-1 flex flex-col min-h-screen overflow-x-hidden">
          {children}
        </main>
        
        </SessionWrapper>
      </body>
    </html>
  );
}

function NavItem({ href, icon, label, active = false }: { href: string, icon: React.ReactNode, label: string, active?: boolean }) {
  return (
    <Link href={href} className={`flex items-center gap-3 px-3 py-2.5 rounded-lg transition-all duration-200 ${active ? 'bg-white/10 text-white shadow-sm ring-1 ring-white/10' : 'text-zinc-400 hover:text-white hover:bg-white/5'}`}>
      {icon}
      <span className="text-sm font-medium">{label}</span>
    </Link>
  );
}
