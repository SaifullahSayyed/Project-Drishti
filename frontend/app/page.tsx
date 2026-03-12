"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { motion } from "framer-motion";

export default function Home() {
  const router = useRouter();
  const [cnr, setCnr] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (cnr.length !== 16) {
      setError("Please enter a valid 16-character CNR number.");
      return;
    }
    setError("");
    setLoading(true);
    // Push to the dynamic case route which handles data fetching
    router.push(`/case/${cnr}`);
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-[85vh] text-center w-full">
      <motion.div 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        className="w-full max-w-2xl px-4"
      >
        <div className="mb-4 inline-flex items-center gap-2 px-3 py-1 rounded-full bg-accent/10 border border-accent/20 text-accent text-sm font-medium">
          <span className="w-2 h-2 rounded-full bg-accent animate-pulse"></span>
          Hackathon Prototype 2026
        </div>
        
        <h1 className="text-5xl md:text-7xl font-extrabold tracking-tight mb-6">
          India's First <br />
          <span className="text-gradient hover:scale-105 transition-transform cursor-default block mt-2">
            Predictive Justice
          </span>
          Engine
        </h1>
        
        <p className="text-lg md:text-xl text-slate-300 mb-10 max-w-xl mx-auto leading-relaxed">
          AI-driven insights for faster case resolution. 
          Enter your 16-digit CNR number to get outcome probabilities, estimated timelines, and recommended alternative dispute resolution pathways.
        </p>

        <form onSubmit={handleSubmit} className="w-full relative group">
          <div className="absolute inset-0 bg-gradient-to-r from-accent to-indigo-500 rounded-2xl blur opacity-25 group-hover:opacity-40 transition duration-500"></div>
          <div className="relative glass-panel rounded-2xl p-2 flex flex-col sm:flex-row gap-2">
            <input
              type="text"
              value={cnr}
              onChange={(e) => setCnr(e.target.value.toUpperCase().replace(/[^A-Z0-9]/g, ""))}
              placeholder="Enter 16-digit CNR (e.g. MHCC010123452023)"
              className="flex-1 bg-transparent border-none text-white px-6 py-4 outline-none placeholder:text-slate-500 text-lg uppercase tracking-wider"
              maxLength={16}
            />
            <button
              type="submit"
              disabled={loading}
              className="px-8 py-4 bg-gradient-to-r from-accent to-indigo-500 rounded-xl font-bold text-white shadow-lg hover:shadow-accent/30 transition-all disabled:opacity-50 disabled:cursor-not-allowed whitespace-nowrap"
            >
              {loading ? (
                <div className="flex items-center gap-2">
                  <span className="w-4 h-4 border-2 border-white/20 border-t-white rounded-full animate-spin"></span>
                  Processing
                </div>
              ) : "Analyze Case"}
            </button>
          </div>
          {error && (
            <motion.p 
              initial={{ opacity: 0 }} 
              animate={{ opacity: 1 }} 
              className="text-red-400 mt-4 text-sm font-medium"
            >
              {error}
            </motion.p>
          )}
        </form>
        
        <div className="mt-16 grid grid-cols-1 md:grid-cols-3 gap-6 text-left">
          {[
            { title: "XGBoost Outcomes", desc: "Machine learning model trained on 10,000+ past judgements." },
            { title: "Smart Pathways", desc: "Automated routing to Lok Adalat or Mediation to save costs." },
            { title: "LLM Summary", desc: "Complex legal precedents simplified by Groq LLaMA 3 API." }
          ].map((feature, i) => (
             <motion.div 
               key={i}
               initial={{ opacity: 0, y: 20 }}
               animate={{ opacity: 1, y: 0 }}
               transition={{ duration: 0.6, delay: 0.2 + (i * 0.1) }}
               className="glass-panel p-6 rounded-2xl border border-white/5 hover:border-accent/30 transition-colors"
             >
               <h3 className="text-white font-bold mb-2">{feature.title}</h3>
               <p className="text-slate-400 text-sm">{feature.desc}</p>
             </motion.div>
          ))}
        </div>
      </motion.div>
    </div>
  );
}
