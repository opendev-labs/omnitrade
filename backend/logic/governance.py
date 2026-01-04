from typing import Dict

def calculate_health_score(metrics: Dict, uncertainty: str) -> int:
    """
    Health = 100 - Drawdown % - Loss Cluster Penalty - Correlation Stress - Uncertainty Penalty
    """
    base = 100
    
    # Metrics impact
    drawdown_penalty = metrics.get("drawdown", 0) * 10
    stress_penalty = metrics.get("correlation_stress", 0) * 10
    
    # Uncertainty impact
    uncertainty_penalty = 0
    if uncertainty == "HIGH":
        uncertainty_penalty = 20
    elif uncertainty == "CRITICAL":
        uncertainty_penalty = 80
        
    health = base - drawdown_penalty - stress_penalty - uncertainty_penalty
    
    return max(0, min(100, int(health)))

def get_governance_mode(health: int) -> str:
    if health >= 80:
        return "FULL"
    elif health >= 60:
        return "REDUCED"
    elif health >= 40:
        return "DEFENSIVE"
    else:
        return "STOP"
