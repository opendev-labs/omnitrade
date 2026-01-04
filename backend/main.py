import asyncio
import json
import time
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict

from .logic.scanners import get_market_state, get_clock_cycle, get_token_rotation, get_correlation_data, get_uncertainty_level
from .logic.bots import TRADING_BOTS, check_bot_triggers
from .logic.governance import calculate_health_score, get_governance_mode

app = FastAPI(title="Omnitrade Backend")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global state for simulation
state = {
    "metrics": {"drawdown": 0.42, "correlation_stress": 0.08, "exposure": 12.5},
    "logs": [
        {"id": "1", "bot": "VWAP REVERSION", "action": "Entry Detected", "status": "SUCCESS", "timestamp": "16:02:11"},
    ]
}

@app.get("/")
async def root():
    return {"status": "online", "system": "Omnitrade OS"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # 1. Gather Scanner Data
            market = get_market_state()
            clock = get_clock_cycle()
            rotation = get_token_rotation()
            correlation = get_correlation_data()
            uncertainty = get_uncertainty_level(state["logs"])
            
            scanners = {**market, **clock}
            
            # 2. Check Bot Triggers
            new_actions = check_bot_triggers(scanners, TRADING_BOTS)
            for action in new_actions:
                action["id"] = str(time.time())
                action["timestamp"] = time.strftime("%H:%M:%S")
                state["logs"].insert(0, action)
            
            # Keep logs manageable
            state["logs"] = state["logs"][:20]
            
            # 3. Governance Logic
            health = calculate_health_score(state["metrics"], uncertainty)
            mode = get_governance_mode(health)
            
            # 4. Construct Payload
            payload = {
                "scanners": {
                    **scanners,
                    "uncertainty": uncertainty,
                    "rotation": rotation,
                    "correlation": correlation
                },
                "bots": [bot.__dict__ for bot in TRADING_BOTS],
                "health": health,
                "mode": mode,
                "metrics": state["metrics"],
                "logs": state["logs"]
            }
            
            await websocket.send_json(payload)
            await asyncio.sleep(2)  # Update every 2 seconds
            
    except WebSocketDisconnect:
        print("Client disconnected")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
