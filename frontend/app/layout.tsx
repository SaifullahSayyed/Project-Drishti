import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({ subsets: ["latin"], variable: "--font-inter" });

export const metadata: Metadata = {
  title: "DRISHTI | Predictive Justice Engine",
  description: "India's First Predictive Justice & Case Resolution Engine",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={`${inter.variable} antialiased selection:bg-accent selection:text-white`}>
        {/* Navigation Bar */}
        <nav className="fixed w-full z-50 glass-panel border-b border-white/5 px-6 py-4">
          <div className="max-w-7xl mx-auto flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-8 h-8 rounded-full bg-gradient-to-tr from-accent to-indigo-500 flex items-center justify-center font-bold text-lg pointer-events-none shadow-lg shadow-accent/20">
                D
              </div>
              <span className="text-xl font-bold tracking-widest text-white/90">DRISHTI</span>
            </div>
            <div className="hidden md:flex items-center gap-6 text-sm font-medium text-white/60">
              <a href="/" className="hover:text-white transition-colors">Home</a>
              <a href="#" className="hover:text-white transition-colors">Pathways</a>
              <a href="#" className="hover:text-white transition-colors">Analysis</a>
              <button className="px-4 py-2 bg-white/10 hover:bg-white/20 rounded-lg text-white transition-colors border border-white/10">
                Sign In
              </button>
            </div>
          </div>
        </nav>
        
        {/* Main Content */}
        <main className="pt-24 pb-12 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
          {children}
        </main>
      </body>
    </html>
  );
}
