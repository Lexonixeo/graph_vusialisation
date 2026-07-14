import pygame

import graph
import camera
import main
import physics


class Visualiser:
    def __init__(self, g: graph.Graph, s: dict):
        self.step = 0
        self.screen_width = s["start_screen_width"]
        self.screen_height = s["start_screen_height"]
        self.screen_name = s["screen_name"]
        self.g = g
        self.pe = physics.PhysicsEngine(g, s)
        self.c = camera.Camera(s)
        self.s = s

        pygame.init()
        self.font = pygame.font.SysFont(s["font_name"], s["font_size"])
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.RESIZABLE)
        pygame.display.set_caption(self.screen_name)
        pygame.display.set_icon(pygame.image.load('images/icon.png'))

    def update(self):
        self.pe.update(self.step)

    # Можно каждому ноду сопоставить pygame.surface уже заранее отрисованный. (рисовать через pygame.surface.blit)
    # Я не знаю где их можно хранить, когда ноды добавляются/убираются.
    # Пускай я просто реализую через pygame.draw
    def draw_node(self, n: graph.Node):
        center = self.c.graph_to_pix(n.point.position)
        pygame.draw.circle(self.screen, self.s["bg_color"], center, self.s["node_radius"])
        pygame.draw.circle(self.screen, self.s["node_color"], center, self.s["node_radius"], self.s["node_width"])

        if self.s["draw_text"]:
            text = self.font.render(str(n.node_id), False, self.s["node_color"])
            self.screen.blit(text, (center[0] - self.s["node_radius"] // 2, center[1] - self.s["node_radius"]))

    def draw_edge(self, u_id, v_id):
        pos1 = self.c.graph_to_pix(self.g.nodes[u_id].point.position)
        pos2 = self.c.graph_to_pix(self.g.nodes[v_id].point.position)
        pygame.draw.line(self.screen, self.s["node_color"], pos1, pos2, self.s["edge_width"])
        # рисовать ли вес ребра?

    def draw(self):
        self.screen.fill(self.s["bg_color"])

        # сначала рёбра, потом вершины
        for u_id in self.g.nodes.keys():
            for v_id in self.g.edges[u_id].keys():
                if v_id > u_id:
                    self.draw_edge(u_id, v_id)

        for node in self.g.nodes.values():
            self.draw_node(node)

    # разделить ивенты на def?
    # добавить скриншот?
    # добавить проверку на то, остановилось ли всё? - сумма кинетических энергий
    def run(self):
        flag_running = True
        while flag_running:
            self.step += 1
            self.update()
            self.draw()
            pygame.display.update()
            for event in pygame.event.get():
                match event.type:
                    case pygame.QUIT:
                        pygame.quit()
                        flag_running = False
                    case pygame.VIDEORESIZE:
                        self.screen_width = event.w
                        self.screen_height = event.h
                        self.c.update_screen_size(self.screen_width, self.screen_height)
                        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.RESIZABLE)
                    case pygame.KEYDOWN:
                        match event.key:
                            case pygame.K_r:
                                self.g.random_shuffle()
                    case pygame.MOUSEBUTTONDOWN:
                        pass
                    case pygame.MOUSEWHEEL:
                        # поворот вперед
                        self.c.scaling(pygame.mouse.get_pos(), event.y)


if __name__ == '__main__':
    # g = graph.generate_graph(10, 12)
    g = graph.generate_graph(main.s, 15, 15)
    v = Visualiser(g, main.s)
    v.run()
    pass
