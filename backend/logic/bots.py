from typing import List, Dict, Optional
from dataclasses import dataclass

@dataclass
class BotConfig:
    id: str
    name: str
    trigger: str
    description: str
    active: bool
    risk: str
    isGuardian: bool = False

TRADING_BOTS = [
    BotConfig("1", "VWAP MEAN REVERSION", "Price ±2σ from VWAP", "Institutional mean reversion for high-liquidity pairings.", True, "LOW"),
    BotConfig("2", "VOLATILITY BREAKOUT", "BB Squeeze + Vol Expansion", "Breakout capture for regime shifts in major assets.", True, "MEDIUM"),
    BotConfig("3", "TREND PULLBACK", "0.5 - 0.618 Fib Retrace", "Captures quality pullbacks in established trend cycles.", False, "LOW"),
    BotConfig("4", "RANGE SCALPER", "Session Range Extremes", "Micro-range execution within session boundaries.", False, "MEDIUM"),
    BotConfig("5", "LIQUIDITY SWEEP", "Equal H/L + RSI Div", "Fades false liquidity grabs at structural extremes.", True, "MEDIUM"),
    BotConfig("6", "SESSION OPEN ALPHA", "Volatility Spike at Open", "Regime-based momentum at major market session starts.", True, "HIGH"),
    BotConfig("7", "FUNDING ARBITRAGE", "Extreme Rates + Price Stall", "Counter-trend capture of over-leveraged positioning.", False, "HIGH"),
    BotConfig("8", "CORRELATION BREAK", "ETH vs BTC Decoupling", "Inter-market divergence strategy for major alts.", False, "LOW"),
    BotConfig("9", "MOMENTUM MICRO", "5m / 15m Alignment", "Low timeframe momentum tracking for agile exposure.", True, "HIGH"),
    BotConfig("10", "NO-TRADE GUARDIAN", "GOVERNANCE LOCK", "Total system circuit breaker. Overrides all execution logic.", False, "HIGH", True),
]

def check_permission_matrix(bot_name: str, scanners: Dict) -> bool:
    """
    Simulates checking against the Sheet Permission Matrix.
    """
    health = 70 # Mocked, should come from state if integrated deeper
    volatility = scanners.get("volatility", "LOW")
    trend = scanners.get("trend", "NEUTRAL")
    phase = scanners.get("phase", "ACCUMULATION")
    
    # Guardian always checks health
    if bot_name == "NO-TRADE GUARDIAN":
        return True # Always runs to check conditions
        
    # Example Rules from Permission Matrix
    if bot_name == "VWAP MEAN REVERSION":
        return trend == "NEUTRAL" and volatility == "LOW"
    elif bot_name == "VOLATILITY BREAKOUT":
        return volatility == "LOW" # Logic: enter when vol is expanding from low
    elif bot_name == "TREND PULLBACK":
        return trend == "UP" and phase == "EXPANSION"
    elif bot_name == "RANGE SCALPER":
        return phase == "ACCUMULATION" and volatility == "LOW"
        
    return True # Default allow for others for now

def check_bot_triggers(scanners: Dict, bots: List[BotConfig]) -> List[Dict]:
    """Simulates bot execution logic based on scanner states"""
    executed_actions = []
    
    # Guardian Logic
    guardian_active = any(b.active for b in bots if b.name == "NO-TRADE GUARDIAN")
    if guardian_active and scanners.get("health", 100) < 40:
        return [{"bot": "NO-TRADE GUARDIAN", "action": "HALT TRADING - HEALTH CRITICAL", "status": "WARNING"}]

    volatility = scanners.get("volatility", "LOW")
    cycle = scanners.get("cycle", "MID")
    
    for bot in bots:
        if not bot.active:
            continue
            
        # Check Permission Matrix
        if not check_permission_matrix(bot.name, scanners):
            continue
            
        # Trigger Logic
        if bot.name == "VOLATILITY BREAKOUT" and volatility == "HIGH":
             executed_actions.append({"bot": bot.name, "action": "Breakout Confirmed", "status": "SUCCESS"})
             
        elif bot.name == "SESSION OPEN ALPHA" and scanners.get("clock") in ["LONDON", "NY"] and cycle == "EARLY":
             executed_actions.append({"bot": bot.name, "action": "Open Range Break", "status": "SUCCESS"})
             
        elif bot.name == "VWAP MEAN REVERSION" and scanners.get("uncertainty") == "LOW":
             # Randomly trigger for simulation if conditions met
             import random
             if random.random() < 0.05:
                executed_actions.append({"bot": bot.name, "action": "Mean Reversion Entry", "status": "SUCCESS"})

    return executed_actions
