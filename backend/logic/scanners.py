import random
import time
from enum import Enum
from typing import Dict, List, Literal

class MarketPhase(str, Enum):
    ACC = 'ACCUMULATION'
    EXP = 'EXPANSION'
    DIST = 'DISTRIBUTION'
    RESET = 'RESET'

class TrendState(str, Enum):
    UP = 'UP'
    DOWN = 'DOWN'
    NEUTRAL = 'NEUTRAL'

class ClockSession(str, Enum):
    ASIA = 'ASIA'
    LONDON = 'LONDON'
    NY = 'NY'

def get_market_state() -> Dict:
    """Simulates Market State Scanner (ATR, EMA, Phase)"""
    return {
        "volatility": "HIGH" if random.random() > 0.7 else "LOW",
        "trend": random.choice(list(TrendState)),
        "phase": random.choice(list(MarketPhase))
    }

def get_clock_cycle() -> Dict:
    """Calculates Clock Cycle Scanner (Session based on UTC/Server time)"""
    hour = time.gmtime().tm_hour
    if 0 <= hour < 8:
        session = ClockSession.ASIA
    elif 8 <= hour < 16:
        session = ClockSession.LONDON
    else:
        session = ClockSession.NY
    
    cycle = "EARLY" if hour % 8 < 2 else ("LATE" if hour % 8 > 6 else "MID")
    
    return {
        "clock": session,
        "cycle": cycle
    }

def get_token_rotation() -> List[Dict]:
    """Simulates Token Rotation Scanner (Relative Strength vs BTC)"""
    tokens = ["SOL", "ETH", "AVAX", "LINK", "EGLD", "MATIC", "DOT"]
    rotation = []
    for t in tokens:
        rotation.append({
            "ticker": t,
            "strength": round(random.uniform(-5, 10), 2),
            "status": "NEXT_PHASE" if random.random() > 0.8 else "TOP_PHASE"
        })
    return sorted(rotation, key=lambda x: x["strength"], reverse=True)

def get_correlation_data() -> Dict:
    """Simulates Correlation Scanner"""
    return {
        "cluster_a": ["SOL", "AVAX", "EGLD"],
        "cluster_b": ["ETH", "OP", "ARB"],
        "stress_index": round(random.random(), 2)
    }

def get_uncertainty_level(logs: List[Dict]) -> str:
    """Calculates Uncertainty Scanner (Signal disagreement, loss cluster)"""
    # Simple logic: if recent logs have many ERRORS, uncertainty rises
    error_count = sum(1 for log in logs if log.get("status") == "ERROR")
    if error_count > 3:
        return "CRITICAL"
    elif error_count > 1:
        return "HIGH"
    return "LOW"
