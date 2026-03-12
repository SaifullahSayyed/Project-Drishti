"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import { motion } from "framer-motion";

export default function CaseDashboard() {
  const { cnr } = useParams();
  const router = useRouter();
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!cnr) return;
    
    // In a real app we'd use React Query. For hackathon speed, simple fetch
    const fetchData = async () => {
      try {
        setLoading(true);
        // Default FastAPI local url
        const res = await fetch(`http://localhost:8000/api/predict/${cnr}`);
        if (!res.ok) {
          throw new Error(res.status === 404 ? "Case not found." : "Server error analyzing case.");
        }
        const json = await res.json();
        setData(json);
      } catch (err: any) {
        setError(err.message || "Failed to fetch data.");
      } finally {
        setLoading(false);
      }
    };
    
    fetchData();
  }, [cnr]);

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh]">
        <div className="w-16 h-16 border-4 border-accent/20 border-t-accent rounded-full animate-spin mb-6"></div>
        <h2 className="text-2xl font-bold text-white mb-2">Analyzing Case Ecosystem</h2>
        <p className="text-slate-400 text-center max-w-md">
          DRISHTI is traversing government matrices, running XGBoost predictions, and consulting Indian Kanoon precedents...
        </p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="glass-panel p-8 rounded-2xl text-center max-w-lg mx-auto mt-20">
        <div className="w-16 h-16 bg-red-500/20 text-red-500 rounded-full flex items-center justify-center mx-auto mb-4 text-3xl font-bold">!</div>
        <h2 className="text-xl font-bold text-white mb-2">Analysis Failed</h2>
        <p className="text-slate-400 mb-6">{error}</p>
        <button onClick={() => router.push("/")} className="px-6 py-3 bg-white/10 hover:bg-white/20 rounded-xl text-white transition-colors">
          Return Home
        </button>
      </div>
    );
  }

  if (!data) return null;

  return (
    <div className="space-y-8 pb-20 fade-in">
      {/* Header Profile */}
      <header className="flex flex-col md:flex-row md:items-end justify-between gap-6 pb-6 border-b border-white/10 mt-8">
        <div>
          <div className="flex items-center gap-3 mb-2">
            <span className="px-3 py-1 bg-accent/20 text-accent text-xs font-bold rounded-full border border-accent/30 uppercase tracking-wider">
              {data.case_data.case_type.replace("_", " ")}
            </span>
            <span className="text-slate-400 text-sm">{data.case_data.district} District</span>
          </div>
          <h1 className="text-3xl md:text-5xl font-extrabold text-white tracking-tight">CNR: {cnr}</h1>
          <p className="text-slate-400 mt-2">Filed: {data.case_data.filing_year} | Expected Value: ₹{data.case_data.claim_value_inr.toLocaleString()}</p>
        </div>
        
        <a 
          href={`http://localhost:8000${data.citizen_report_url}`}
          target="_blank"
          className="px-6 py-3 bg-white text-slate-900 font-bold rounded-xl hover:bg-slate-200 transition-colors shadow-lg flex items-center justify-center gap-2"
        >
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" /></svg>
          Download Citizen Report PDF
        </a>
      </header>

      {/* RAG Executive Summary */}
      <motion.section 
        initial={{ y: 20, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ delay: 0.1 }}
        className="glass-panel p-6 md:p-8 rounded-2xl relative overflow-hidden"
      >
        <div className="absolute top-0 right-0 w-64 h-64 bg-accent/10 rounded-full blur-[80px]"></div>
        <h2 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
          <span className="w-2 h-2 rounded-full bg-accent"></span> AI Executive Summary
        </h2>
        <div className="text-slate-300 text-lg leading-relaxed whitespace-pre-wrap relative z-10">
          {data.rag_summary}
        </div>
      </motion.section>

      {/* Metrics Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {[
          { label: "Petitioner Win Prob.", value: `${data.outcome.petitioner_win_prob}%`, color: "text-green-400" },
          { label: "Est. Resolution Time", value: `${data.outcome.estimated_years} yrs`, sub: `Range: ${data.outcome.range_min}-${data.outcome.range_max} yrs`, color: "text-white" },
          { label: "District Average", value: `${data.outcome.district_avg} yrs`, color: "text-white" },
          { label: "Prediction Confidence", value: `${data.outcome.confidence_score}%`, color: "text-accent" },
        ].map((stat, i) => (
          <motion.div 
            key={i}
            initial={{ y: 20, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 0.2 + (i * 0.1) }}
            className="glass-panel p-6 rounded-2xl flex flex-col justify-center"
          >
            <p className="text-slate-400 text-sm font-medium mb-1">{stat.label}</p>
            <h3 className={`text-3xl font-extrabold ${stat.color}`}>{stat.value}</h3>
            {stat.sub && <p className="text-xs text-slate-500 mt-2">{stat.sub}</p>}
          </motion.div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        
        {/* Recommended Pathway */}
        <motion.section 
          initial={{ x: -20, opacity: 0 }}
          animate={{ x: 0, opacity: 1 }}
          transition={{ delay: 0.4 }}
          className="glass-panel p-6 rounded-2xl border border-success/20 bg-success/5"
        >
          <div className="flex items-center justify-between mb-6">
             <h2 className="text-xl font-bold text-white">Recommended Pathway</h2>
             <span className="px-3 py-1 bg-success/20 text-success text-xs font-bold rounded-full">OPTIMAL</span>
          </div>
          
          <div className="mb-6">
            <h3 className="text-4xl font-extrabold text-white mb-2">{data.pathway.recommended}</h3>
            <p className="text-success font-medium">Saves an estimated ₹{data.pathway.cost_saving_inr.toLocaleString()} vs standard trial details</p>
          </div>

          <div className="space-y-4">
             <div className="bg-black/30 p-4 rounded-xl">
               <p className="text-sm text-slate-400 mb-1">Reason for Recommendation</p>
               <p className="text-white font-medium">{data.pathway.eligibility_reason}</p>
             </div>
             
             <div className="bg-black/30 p-4 rounded-xl">
               <p className="text-sm text-slate-400 mb-1">Action Step</p>
               <p className="text-white font-medium">{data.pathway.how_to_apply}</p>
               <p className="text-accent text-sm mt-2">→ {data.pathway.nearest_centre}</p>
             </div>
          </div>
        </motion.section>

        {/* Bottlenecks */}
        <motion.section 
          initial={{ x: 20, opacity: 0 }}
          animate={{ x: 0, opacity: 1 }}
          transition={{ delay: 0.5 }}
          className="glass-panel p-6 rounded-2xl"
        >
          <h2 className="text-xl font-bold text-white mb-6">Process Bottleneck Risks</h2>
          <div className="space-y-4">
            {data.bottlenecks.map((btn: any, i: number) => (
              <div key={i} className="bg-black/20 border border-white/5 p-4 rounded-xl">
                <div className="flex justify-between items-start mb-2">
                   <h4 className="text-white font-bold">{btn.name}</h4>
                   <span className={`text-xs font-bold px-2 py-1 rounded-md ${
                     btn.severity === 'high' ? 'bg-red-500/20 text-red-400' : 'bg-yellow-500/20 text-yellow-500'
                   }`}>
                     {btn.severity.toUpperCase()} RISK ({btn.probability * 100}%)
                   </span>
                </div>
                <p className="text-sm text-slate-400 mb-3">Expected Delay Impact: <span className="text-white">{btn.avg_delay_months} months</span></p>
                <div className="px-3 py-2 bg-accent/10 rounded-lg border border-accent/20">
                  <p className="text-xs text-accent font-medium">🛡️ Mitigation: {btn.mitigation}</p>
                </div>
              </div>
            ))}
            {data.bottlenecks.length === 0 && (
              <p className="text-slate-400 italic">No major delays predicted for this jurisdiction.</p>
            )}
          </div>
        </motion.section>

      </div>

    </div>
  );
}
