#!/usr/bin/env python3
import asyncio
import websockets
import json
import requests
import time

BACKEND_URL = "http://localhost:8000"
WS_URL = "ws://localhost:8000/ws"

def test_rest_root():
    print("Testing REST Root...")
    try:
        response = requests.get(BACKEND_URL)
        assert response.status_code == 200
        assert response.json()["system"] == "Omnitrade OS"
        print("✅ REST Root Passed")
    except Exception as e:
        print(f"❌ REST Root Failed: {e}")

async def test_websocket():
    print("Testing WebSocket Stream...")
    try:
        async with websockets.connect(WS_URL) as websocket:
            # Receive at least 3 messages to verify stream consistency
            for i in range(3):
                message = await websocket.recv()
                data = json.loads(message)
                
                # Verify schema
                assert "scanners" in data
                assert "bots" in data
                assert "health" in data
                assert "mode" in data
                
                print(f"✅ WebSocket Message {i+1} received: Health={data['health']}, Mode={data['mode']}")
            
            print("✅ WebSocket Stream Passed")
    except Exception as e:
        print(f"❌ WebSocket Failed: {e}")

if __name__ == "__main__":
    # Wait for server to be ready
    time.sleep(2)
    test_rest_root()
    asyncio.run(test_websocket())
