import pygame
import json
import asyncio
import websockets

WIDTH, HEIGHT = 500, 500
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

async def main():
    async with websockets.connect("ws://YOUR_SERVER_IP:5000") as websocket:
        pygame.init()
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        clock = pygame.time.Clock()

        running = True
        player_id = None
        players = {}

        # Game loop
        while running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Update player position
            keys = pygame.key.get_pressed()
            if player_id:
                if keys[pygame.K_UP]:
                    players[player_id][1] -= 5
                if keys[pygame.K_DOWN]:
                    players[player_id][1] += 5
                if keys[pygame.K_LEFT]:
                    players[player_id][0] -= 5
                if keys[pygame.K_RIGHT]:
                    players[player_id][0] += 5

                # Send updated position to server
                await websocket.send(json.dumps({"position": players[player_id]}))

            # Receive data from server
            try:
                message = await websocket.recv()
                data = json.loads(message)
                if "id" in data:
                    player_id = data["id"]
                players = data["players"]
            except:
                pass

            # Render the game
            screen.fill(WHITE)
            for pid, pos in players.items():
                color = BLUE if pid == player_id else RED
                pygame.draw.rect(screen, color, (*pos, 50, 50))
            pygame.display.flip()
            clock.tick(30)

        pygame.quit()

asyncio.run(main())
