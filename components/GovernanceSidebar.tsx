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
        <h2 className="text-xs font-bold uppercase tracking-[0.5em] text-secondary opacity-60">Risk Audit</h2>
        <span className="text-xs text-secondary font-mono-data font-bold opacity-40">V_4.2.X</span>
      </div>

      {/* High-Precision Health Gauge */}
      <div className="terminal-panel p-8 lg:p-12 rounded-sm flex flex-col items-center">
        <div className="relative w-36 h-36 lg:w-44 lg:h-44 flex items-center justify-center">
          <svg className="w-full h-full transform -rotate-90 drop-shadow-[0_0_10px_rgba(var(--accent-rgb),0.3)]" viewBox="0 0 100 100">
            {/* Track */}
            <circle cx="50" cy="50" r="44" stroke="var(--border)" strokeWidth="2" fill="transparent" opacity="0.2" />
            {/* Progress */}
            <circle
              cx="50" cy="50" r="44" stroke="var(--text-secondary)" strokeWidth="4" fill="transparent"
              strokeDasharray="276.46"
              strokeDashoffset={`${276.46 * (1 - healthScore / 100)}`}
              strokeLinecap="round"
              className="transition-all duration-1000 ease-[var(--easing)]"
              style={{ stroke: 'var(--accent)' }}
            />
          </svg>
          <div className="absolute inset-0 flex flex-col items-center justify-center">
            <span className="text-5xl lg:text-7xl font-bold tracking-tighter text-accent leading-none drop-shadow-[0_0_8px_rgba(var(--accent-rgb),0.5)]">{healthScore}</span>
            <span className="text-xs lg:text-sm text-secondary font-bold uppercase tracking-[0.5em] mt-3 lg:mt-4 opacity-80">Health Idx</span>
          </div>
        </div>

        <div className="w-full mt-10 lg:mt-16 space-y-6 lg:space-y-8">
          <div className="flex justify-between items-center py-4 lg:py-6 border-b border-white/10">
            <span className="text-xs lg:text-sm font-bold text-muted uppercase tracking-[0.4em]">Protocol</span>
            <span className="text-sm lg:text-base font-bold uppercase text-primary">{mode}</span>
          </div>
          <div className="flex justify-between items-center py-4 lg:py-6 border-b border-white/10">
            <span className="text-xs lg:text-sm font-bold text-muted uppercase tracking-[0.4em]">Drawdown</span>
            <span className="text-sm lg:text-base font-bold text-primary font-mono-data">-{metrics.drawdown.toFixed(2)}%</span>
          </div>
        </div>
      </div>

      {/* Minimalist Audit Log */}
      <div className="flex flex-col flex-1 overflow-hidden min-h-[300px]">
        <div className="flex justify-between items-center mb-6 lg:mb-8 px-1 border-b border-white/10 pb-3">
          <span className="text-xs font-bold text-muted uppercase tracking-[0.4em]">Telemetry Audit</span>
          <div className="w-1.5 h-1.5 rounded-full bg-accent opacity-20"></div>
        </div>
        <div className="flex-1 overflow-y-auto space-y-px custom-scrollbar">
          {logs.map(log => (
            <div key={log.id} className="p-3 lg:p-4 border-b border-white/5 hover:bg-neutral-900/10 transition-all duration-700 group">
              <div className="flex justify-between items-center mb-2 lg:mb-3">
                <span className="text-xs lg:text-sm font-bold text-secondary tracking-tighter uppercase">{log.bot}</span>
                <span className="text-xs text-muted font-mono-data font-bold">{log.timestamp}</span>
              </div>
              <div className="flex items-center gap-3 lg:gap-4">
                <div className={`w-2 h-2 rounded-full ${log.status === 'SUCCESS' ? 'bg-accent opacity-50' : 'bg-red-500'}`}></div>
                <span className="text-xs lg:text-sm text-muted font-bold tracking-tight uppercase leading-none">{log.action}</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default GovernanceSidebar;