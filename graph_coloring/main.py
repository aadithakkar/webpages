import pygame, sys, math, time, asyncio

pygame.init()

screen = pygame.display.set_mode([800, 800])
pygame.display.set_caption("Graph Coloring")

COLORS = [(200, 0, 0), (0, 200, 0), (0, 0, 200), (200, 200, 0)]

class Vertex:
    def __init__(self, x, y, id):
        self.x = x
        self.y = y
        self.edges = []
        self.adj = []
        self.dragging = 0
        self.num = id
        self.selected = False
        self.col = None
        self.active = 0
        self.col_candidates = [0, 1, 2, 3]
        self.colindex = None
        self.parent = None
        self.failed = 0
        self.color = None
        self.possible = [0, 1, 2, 3]
        self.color = -1
        self.gx, self.gy = x, y
    def draw(self):
        self.col = self.color
        pygame.draw.circle(screen, (200, 200, 200), (self.x, self.y), 20)
        col = (18, 18, 18)
        if self.selected:
            col = (0, 150, 200)
        elif self.col >= 0:
            col = COLORS[self.col]
        pygame.draw.circle(screen, col, (self.x, self.y), 15)
    def update(self):
        if self.gx != self.x:
            # print('ud')
            self.x += (self.gx - self.x) * 0.1
            if abs(self.gx - self.x) <= 2:
                self.x = self.gx
                self.gx = self.x
        if self.gy != self.y:
            self.y += (self.gy - self.y) * 0.1
            if abs(self.gy - self.y) <= 2:
                self.y = self.gy
                self.gy = self.y
        if self.dragging:
            self.x, self.y = pygame.mouse.get_pos()
            self.gx, self.gy = self.x, self.y
        if self.failed:
            self.colindex += 1
            self.find_col()
        if self.active:
            for adj in self.adj:
                if adj.col is not None:
                    if adj.col in self.col_candidates:
                        self.col_candidates.remove(adj.col)
                else:
                    adj.parent = self
                    adj.active = 1
            self.colindex = 0
            self.find_col()
    def find_col(self):
        if self.colindex >= len(self.col_candidates):
            self.parent.failed = 1
            # print("nothing possible!")
            self.active = 0
            return
        self.col = self.col_candidates[self.colindex]
        # print(self.num, self.col)
        self.active = 0
    def find_coloring(self, stime, first=1):
        if time.time() - stime > 4:
            raise TimeoutError
        if self.color >= 0:
            return True
        if first:
            possible = [0]
        else:
            possible = [0, 1, 2, 3]
        for adj in self.adj:
            if adj.color >= 0 and adj.color in possible:
                possible.remove(adj.color)
        # print(f"vertex {self.num} has possiblities: {possible}")
        for col in possible:
            self.color = col
            # print(f"vertex {self.num} trying {self.color}")
            for adj in self.adj:
                sol_found = adj.find_coloring(stime, 0)
                if not sol_found:
                    # print(f"vertex {self.num} found a contradiction: neighbor {adj.num} couldnt fill the graph.")
                    break
            else:
                # print(f"vertex {self.num} satisfied.")
                return True
        self.color = -1
        return False
            
    
                
class Text(pygame.sprite.Sprite):
    def __init__(self, txt):
        self.groups = all_sprites
        super().__init__(self.groups)
        self.image = pygame.Surface((800, 200)).convert_alpha()
        self.rect = self.image.get_rect()
        self.image.fill((0, 0, 0, 0))
        write(txt, (400, 100), (200, 200, 200), 50, self.image)
        self.alpha = 550
    def update(self):
        self.alpha -= 5
        if self.alpha <= 0:
            self.kill()
            return
        self.image.set_alpha(min(self.alpha, 255))

class Edge:
    def __init__(self, endpoints):
        self.endpoints = endpoints
    def draw(self):
        v = self.endpoints[0]
        x1, y1 = v.x, v.y
        v = self.endpoints[1]
        x2, y2 = v.x, v.y
        pygame.draw.line(screen, (150, 150, 150), (x1, y1), (x2, y2), 8)

class Game:
    def __init__(self):
        self.running = True
        self.clock = pygame.time.Clock()
        self.controls = 0
        self.control_descs = ["CTRL + Click  -  Create New Vertex",
                              "SHIFT + Click  -  Select Vertex / Create Edge",
                              "ENTER  -  Idenitfy 4-Coloring",
                              "/  -  Organize Graph",
                              "BACKSPACE  -  Delete Selected Vertex",
                              "C  -  Clear Colors",
                              "R  -  Reset Simulation"]
        self.reset()
    def reset(self):
        self.vertices = [Vertex(400, 400, 0)]
        self.edges = []
        self.edge_pairs = set()
        self.selected = None
        self.vertexid = 1
    async def run(self):
        while self.running:
            all_sprites.update()
            for vertex in self.vertices:
                vertex.update()
            self.draw_screen(screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.clear()
                        try:
                            if not self.vertices[0].find_coloring(time.time()):
                                Text("No Solution")
                                self.clear()
                        except TimeoutError:
                            # print('timeout.')
                            Text("No Solution Found")
                            self.clear()
                        # self.vertices[0].active = 1
                    elif event.key == pygame.K_c:
                        self.clear()
                    elif event.key == pygame.K_SLASH:
                        n = len(self.vertices)
                        for i in range(n):
                            theta = i / n * (2 * math.pi)
                            x = 400 + math.sin(theta) * 200
                            y = 400 + math.cos(theta) * 200
                            v = self.vertices[i]
                            v.gx, v.gy = x, y
                    elif event.key == pygame.K_r:
                        self.reset()
                    elif event.key == pygame.K_BACKSPACE:
                        if self.selected:
                            self.vertices.remove(self.selected)
                            vertex = self.selected
                            self.selected = None
                            # vn = self.selected.num
                            ne = []
                            for i, edge in enumerate(self.edges):
                                if vertex not in edge.endpoints:
                                    ne.append(edge)
                                else:
                                    w, v = edge.endpoints
                                    w.adj.remove(v)
                                    v.adj.remove(w)
                            self.edges = ne
                    elif event.unicode and event.unicode in "1234":
                        if self.selected:
                            self.selected.color = int(event.unicode) - 1
                            self.selected.selected = False
                            self.selected = None
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.controls:
                        self.controls = 0
                    else:
                        mx, my = pygame.mouse.get_pos()
                        if my < 50 and mx < 150:
                            self.controls = 1
                        else:
                            keys = pygame.key.get_pressed()
                            if keys[pygame.K_LCTRL]:
                                self.vertices.append(Vertex(mx, my, self.vertexid))
                                self.vertexid += 1
                            # elif keys[pygame.K_LSHIFT]:
                            #     if not self.selected:
                            #         self.selected = 
                            else:
                                clicked = None
                                for vertex in self.vertices:
                                    if (mx - vertex.x) ** 2 + (my - vertex.y) ** 2 <= 400:
                                        clicked = vertex
                                        break
                                if clicked:
                                    if keys[pygame.K_LSHIFT]:
                                        if not self.selected:
                                            self.selected = clicked
                                            clicked.selected = True
                                        else:
                                            self.new_edge(self.selected, clicked)
                                            self.selected.selected = False
                                            self.selected = None
                                            # print(self.vertices, self.edge_pairs)
                                    else:
                                        clicked.dragging = 1
                elif event.type == pygame.MOUSEBUTTONUP:
                    for vertex in self.vertices:
                        vertex.dragging = 0
            pygame.display.update()
            self.clock.tick(60)
            await asyncio.sleep(0)
    def draw_screen(self, screen):
        screen.fill((18, 18, 18))
        if not self.controls:
            for edge in self.edges:
                edge.draw()
            for vertex in self.vertices:
                vertex.draw()
            write(f"Order: {len(self.vertices)}", (100, 750), (150, 150, 150), 50, screen)
            write(f"Size: {len(self.edges)}", (700, 750), (150, 150, 150), 50, screen)
            write("CONTROLS", (70, 30), (200, 200, 200), 30, screen)
            all_sprites.draw(screen)
        else:
            for i in range(7):
                write(self.control_descs[i], (400, i * 100 + 100), (200, 200, 200), 50, screen)
    def clear(self):
        for vertex in self.vertices:
            vertex.color = -1
    def new_edge(self, v1, v2):
        if v1.num > v2.num:
            v1, v2 = v2, v1
        elif v1.num == v2.num:
            return
        p = (v1.num, v2.num)
        if p in self.edge_pairs:
            self.edge_pairs.remove(p)
            for edge in self.edges:
                v1, v2 = edge.endpoints
                if (v1.num, v2.num) == p:
                    self.edges.remove(edge)
                    v1.edges.remove(edge)
                    v1.adj.remove(v2)
                    v2.edges.remove(edge)
                    v2.adj.remove(v1)
                    break
            return
        edge = Edge((v1, v2))
        self.edge_pairs.add((v1.num, v2.num))
        self.edges.append(edge)
        v1.edges.append(edge)
        v1.adj.append(v2)
        v2.edges.append(edge)
        v2.adj.append(v1)
        return edge

all_sprites = pygame.sprite.LayeredUpdates()

def write(txt, pos, col, size, surf):
    font = pygame.font.Font(None, size)
    textimg = font.render(str(txt), True, col)
    isize = textimg.get_size()
    surf.blit(textimg, (pos[0]-isize[0]/2, pos[1]-isize[1]/2))

def main():
    asyncio.run(Game().run())

main()
