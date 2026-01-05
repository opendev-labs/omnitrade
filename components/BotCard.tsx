import React from 'react';
import { BotConfig, RiskLevel } from '../types';

interface BotCardProps {
  bot: BotConfig;
  onToggle: (id: string) => void;
  onInitialize: (id: string) => void;
}

const BotCard: React.FC<BotCardProps> = ({ bot, onToggle, onInitialize }) => {
  const isGuardian = bot.isGuardian;

  return (
    <div className={`terminal-panel group relative p-4 lg:p-6 rounded-sm flex flex-col gap-6 lg:gap-8 ${!bot.active && !isGuardian ? 'opacity-30 grayscale' : 'opacity-100'}`}>
      {/* Top Section */}
      <div className="flex justify-between items-start">
        <div className="space-y-1 lg:space-y-2">
          <div className="flex items-center gap-3 lg:gap-4">
            <h3 className={`text-sm lg:text-base font-bold tracking-widest uppercase ${isGuardian ? 'text-accent' : 'text-primary'}`}>
              {bot.name}
            </h3>
            <span className={`text-xs px-2 py-0.5 rounded-full font-bold border border-white/10 text-muted uppercase tracking-[0.1em]`}>
              {bot.risk}
            </span>
          </div>
          <div className="flex items-center gap-3 lg:gap-4 text-xs lg:text-sm font-mono-data text-muted font-bold">
            <span>REG_0x{bot.id}</span>
            <span className="opacity-40">/</span>
            <span>STRAT_ACTIVE</span>
          </div>
        </div>

        <button
          onClick={() => onToggle(bot.id)}
          className={`w-10 h-1.5 lg:w-12 lg:h-1.5 transition-all duration-1000 ease-[var(--easing)] ${bot.active ? (isGuardian ? 'bg-accent shadow-[0_0_8px_var(--accent)]' : 'bg-accent/60') : 'bg-void border border-white/5'}`}
        />
      </div>

      {/* Logic Display */}
      <div className="space-y-4 lg:space-y-6 flex-1">
        <div className="flex flex-col gap-2 lg:gap-3">
          <span className="text-xs font-bold text-muted uppercase tracking-[0.5em]">Trigger_Matrix</span>
          <div className="text-xs lg:text-sm font-mono-data text-secondary leading-none tracking-tight">
            {bot.trigger}
          </div>
        </div>
        <p className="text-xs lg:text-sm text-secondary leading-relaxed font-medium tracking-tight line-clamp-2 min-h-[36px] lg:min-h-[40px]">
          {bot.description}
        </p>
      </div>

      {/* Action Tray */}
      <div className="pt-4 flex gap-4">
        <button
          disabled={!bot.active}
          onClick={() => onInitialize(bot.id)}
          className={`flex-1 py-3 lg:py-4 text-xs lg:text-sm font-bold uppercase tracking-[0.3em] transition-all duration-500 border ${bot.active ? 'bg-void border-white/10 hover:bg-accent hover:text-void text-primary' : 'bg-transparent text-muted border-transparent cursor-not-allowed'}`}
        >
          Initialize
        </button>
        {isGuardian && bot.active && (
          <div className="w-2 h-2 rounded-full bg-accent animate-pulse self-center"></div>
        )}
      </div>
    </div>
  );
};

export default BotCard;