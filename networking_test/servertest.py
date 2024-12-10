import asyncio
import websockets
import json

players = {}  # Store player positions keyed by unique IDs

async def handle_connection(websocket, path):
    player_id = str(len(players))  # Assign a unique ID
    players[player_id] = [200, 200]  # Initial position

    try:
        await websocket.send(json.dumps({"id": player_id, "players": players}))  # Send initial data
        async for message in websocket:
            data = json.loads(message)
            players[player_id] = data["position"]  # Update player's position
            # Broadcast updated player positions to all clients
            await websocket.send(json.dumps({"players": players}))
    except:
        del players[player_id]

server = websockets.serve(handle_connection, "0.0.0.0", 5000)

asyncio.get_event_loop().run_until_complete(server)
asyncio.get_event_loop().run_forever()
