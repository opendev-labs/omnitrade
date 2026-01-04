import React from 'react';
import { GovernanceMode, ExecutionLog, SystemMetrics } from '../types';

interface GovernanceSidebarProps {
  healthScore: number;
  mode: GovernanceMode;
  logs: ExecutionLog[];
  metrics: SystemMetrics;
}

const GovernanceSidebar: React.FC<GovernanceSidebarProps> = ({ healthScore, mode, logs, metrics }) => {
  return (
    <div className="flex flex-col gap-8 lg:gap-10 w-full h-full">
      <div className="flex items-center justify-between px-1">
        <h2 className="text-[10px] font-bold uppercase tracking-[0.5em] text-secondary opacity-60">Risk Audit</h2>
        <span className="text-[9px] text-secondary font-mono-data font-bold opacity-40">V_4.2.X</span>
      </div>

      {/* High-Precision Health Gauge */}
      <div className="terminal-panel p-8 lg:p-12 rounded-sm flex flex-col items-center">
        <div className="relative w-36 h-36 lg:w-44 lg:h-44 flex items-center justify-center">
          <svg className="w-full h-full transform -rotate-90">
            <circle cx="50%" cy="50%" r="48%" stroke="var(--border)" strokeWidth="0.5" fill="transparent" />
            <circle 
              cx="50%" cy="50%" r="47%" stroke="var(--text-secondary)" strokeWidth="1.5" fill="transparent" 
              strokeDasharray="300%" 
              strokeDashoffset={`${300 - (300 * healthScore) / 100}%`}
              className="transition-all duration-1000 ease-[var(--easing)]"
              style={{ stroke: 'var(--accent)' }}
            />
          </svg>
          <div className="absolute inset-0 flex flex-col items-center justify-center">
            <span className="text-4xl lg:text-6xl font-bold tracking-tighter text-accent leading-none">{healthScore}</span>
            <span className="text-[8px] lg:text-[9px] text-secondary font-bold uppercase tracking-[0.5em] mt-2 lg:mt-3">Health Idx</span>
          </div>
        </div>

        <div className="w-full mt-8 lg:mt-12 space-y-4 lg:space-y-5">
          <div className="flex justify-between items-center py-2 lg:py-3 border-b border-white/5">
            <span className="text-[9px] lg:text-[10px] font-bold text-muted uppercase tracking-[0.4em]">Protocol</span>
            <span className="text-[10px] lg:text-[11px] font-bold uppercase text-primary">{mode}</span>
          </div>
          <div className="flex justify-between items-center py-2 lg:py-3 border-b border-white/5">
            <span className="text-[9px] lg:text-[10px] font-bold text-muted uppercase tracking-[0.4em]">Drawdown</span>
            <span className="text-[10px] lg:text-[11px] font-bold text-primary font-mono-data">-{metrics.drawdown.toFixed(2)}%</span>
          </div>
        </div>
      </div>

      {/* Minimalist Audit Log */}
      <div className="flex flex-col flex-1 overflow-hidden min-h-[300px]">
        <div className="flex justify-between items-center mb-4 lg:mb-6 px-1 border-b border-white/5 pb-2">
            <span className="text-[9px] font-bold text-muted uppercase tracking-[0.4em]">Telemetry Audit</span>
            <div className="w-1.5 h-1.5 rounded-full bg-accent opacity-20"></div>
        </div>
        <div className="flex-1 overflow-y-auto space-y-px custom-scrollbar">
          {logs.map(log => (
            <div key={log.id} className="p-3 lg:p-4 border-b border-white/5 hover:bg-neutral-900/10 transition-all duration-700 group">
              <div className="flex justify-between items-center mb-1 lg:mb-2">
                <span className="text-[9px] lg:text-[10px] font-bold text-secondary tracking-tighter uppercase">{log.bot}</span>
                <span className="text-[8px] text-muted font-mono-data font-bold">{log.timestamp}</span>
              </div>
              <div className="flex items-center gap-2 lg:gap-3">
                <div className={`w-1 h-1 rounded-full ${log.status === 'SUCCESS' ? 'bg-accent opacity-50' : 'bg-red-500'}`}></div>
                <span className="text-[9px] lg:text-[10px] text-muted font-bold tracking-tight uppercase leading-none">{log.action}</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default GovernanceSidebar;