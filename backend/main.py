import asyncio
import json
import time
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict

from .logic.scanners import get_market_state, get_clock_cycle, get_token_rotation, get_correlation_data, get_uncertainty_level
from .logic.bots import TRADING_BOTS, check_bot_triggers
from .logic.governance import calculate_health_score, get_governance_mode, apply_auto_rules
from .services.sheets_service import sheets_service

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
    ],
    "sheet_id": "1234567890abcdef", # Default mock ID
    "loss_streak": 0
}

@app.get("/")
async def root():
    return {"status": "online", "system": "Omnitrade OS"}

@app.post("/api/bots/{bot_id}/initialize")
async def initialize_bot(bot_id: str):
    bot = next((b for b in TRADING_BOTS if b.id == bot_id), None)
    if not bot:
        raise HTTPException(status_code=404, detail="Bot not found")
    
    # Toggle bot active state or trigger initialization logic
    # consistently with the plan, we just log it and maybe set active
    bot.active = True # Force active on initialize
    
    log_entry = {
        "id": str(time.time()),
        "bot": bot.name,
        "action": "INITIALIZED MANUALLY",
        "status": "SUCCESS",
        "timestamp": time.strftime("%H:%M:%S")
    }
    state["logs"].insert(0, log_entry)
    state["logs"] = state["logs"][:20]
    
    return {"status": "success", "bot": bot.name}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # 1. Gather Scanner Data (Hybrid: Sheets + Simulated)
            # Fetch from Sheets (Mocked or Real)
            # data = sheets_service.get_market_data(state["sheet_id"], "MARKET_STATE!A2:J") 
            # For now, we mix existing scanners with potential sheet data override
            
            market = get_market_state()
            clock = get_clock_cycle()
            rotation = get_token_rotation()
            correlation = get_correlation_data()
            uncertainty = get_uncertainty_level(state["logs"])
            
            scanners = {**market, **clock}
            
            # 2. Check Bot Triggers (Permission Matrix Check)
            # We would pass the permission matrix here
            
            new_actions = check_bot_triggers(scanners, TRADING_BOTS)
            for action in new_actions:
                action["id"] = str(time.time())
                action["timestamp"] = time.strftime("%H:%M:%S")
                state["logs"].insert(0, action)
            
            # Keep logs manageable
            state["logs"] = state["logs"][:20]
            
            # 3. Governance Logic
            health = calculate_health_score(state["metrics"], uncertainty, state.get("loss_streak", 0))
            mode = get_governance_mode(health)
            
            # Auto Rules Check
            # rules = apply_auto_rules(health, correlation["stress"] > 0.8, uncertainty)
            # if rules["bot_status"] == "ALL_OFF": ... (implement if needed)

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
