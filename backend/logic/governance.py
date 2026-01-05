from typing import Dict, List

def calculate_health_score(metrics: Dict, uncertainty: str, loss_streak: int = 0) -> int:
    """
    Health = 100 - (Current DD * 2) - (Loss Cluster * 10) - (Correlation Stress * 15) - (Uncertainty * 20)
    """
    base = 100
    
    # Metrics impact
    # Assuming drawdown is in percentage (e.g. 5.5 for 5.5%)
    drawdown_penalty = metrics.get("drawdown", 0) * 2
    
    # Loss Cluster Penalty (Streak of losses)
    loss_cluster_penalty = loss_streak * 10
    
    # Correlation Stress (0.0 to 1.0, scaled to impact)
    stress_penalty = metrics.get("correlation_stress", 0) * 100 * 0.15 # Assuming stress is 0-1, 15 max penalty? 
    # Actually prompt says "Correlation Stress * 15". If stress is e.g. 0.8 (high), penalty 12? 
    # Let's assume input stress is 0-1 coeff. 
    stress_penalty = metrics.get("correlation_stress", 0) * 15 
    if metrics.get("correlation_stress", 0) <= 1.0: # If it's normalized 0-1
         stress_penalty = metrics.get("correlation_stress", 0) * 15 * 10 # Re-read: "Correlation Stress * 15". 
         # Let's stick to simple multiplication if the metric provides a 'score' or just strict interpretation.
         # If stress is a coefficient 0.85, 0.85 * 15 = 12.75 points.
    
    # Uncertainty impact
    uncertainty_penalty = 0
    if uncertainty == "HIGH":
        uncertainty_penalty = 20
    elif uncertainty == "CRITICAL":
        uncertainty_penalty = 40 # Escalated
        
    health = base - drawdown_penalty - loss_cluster_penalty - stress_penalty - uncertainty_penalty
    
    return max(0, min(100, int(health)))

def get_governance_mode(health: int) -> str:
    if health > 80:
        return "FULL"
    elif health >= 60:
        return "REDUCED"
    elif health >= 40:
        return "DEFENSIVE"
    else:
        return "STOP"

def apply_auto_rules(health: int, correlation_spike: bool, uncertainty: str) -> Dict:
    """
    Returns governance actions based on rules.
    """
    actions = {
        "bot_status": "ACTIVE",
        "size_reduction": 0.0
    }
    
    if health < 40:
        actions["bot_status"] = "ALL_OFF"
    
    if correlation_spike:
        actions["size_reduction"] = 0.5
        
    if uncertainty == "HIGH":
        actions["bot_status"] = "PAUSED"
        
    return actions
