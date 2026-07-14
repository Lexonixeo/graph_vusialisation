import pygame
import numpy as np
import random

import graph

node_radius = 5  # 20
node_color = (255, 255, 255)
bg_color = (0, 0, 0)
node_circle_width = node_radius  # 5
scaling_base = 2 ** 0.5


class Camera:
    def __init__(self, screen_width, screen_height):
        self.camera_graph_point = (0, 0)
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.camera_pix_point = (screen_width / 2, screen_height / 2)
        self.graph_to_pix_const = 1

    def update_screen_size(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.camera_pix_point = (screen_width / 2, screen_height / 2)

    def graph_to_pix(self, graph_point):
        delta_x = graph_point[0] - self.camera_graph_point[0]
        delta_y = graph_point[1] - self.camera_graph_point[1]
        delta_pix_x = delta_x * self.graph_to_pix_const
        delta_pix_y = -1 * delta_y * self.graph_to_pix_const
        pix_x = self.camera_pix_point[0] + delta_pix_x
        pix_y = self.camera_pix_point[1] + delta_pix_y
        return pix_x, pix_y

    def pix_to_graph(self, pix_point):
        delta_pix_x = pix_point[0] - self.camera_pix_point[0]
        delta_pix_y = pix_point[1] - self.camera_pix_point[1]
        delta_x = delta_pix_x / self.graph_to_pix_const
        delta_y = -1 * delta_pix_y / self.graph_to_pix_const
        x = self.camera_graph_point[0] + delta_x
        y = self.camera_graph_point[1] + delta_y
        return x, y

    def scaling(self, mouse_pos, power):
        coefficient = scaling_base ** power
        radius_vector = np.array(self.camera_graph_point) - np.array(self.pix_to_graph(mouse_pos))
        print(radius_vector)

        self.graph_to_pix_const *= coefficient
        # Сохраняем mouse_pos и mouse_graph_pos, панорамируем как-то

    def panning(self, delta_pix_x, delta_pix_y):
        pass


class Visualiser:
    def __init__(self, graph):
        self.step = 0
        self.graph_to_pix_const = 1
        self.screen_width = 1600
        self.screen_height = 900
        self.screen_name = 'Визуализатор графа'
        self.g = graph
        self.c = Camera(self.screen_width, self.screen_height)

        pygame.init()
        self.font = pygame.font.SysFont('Arial', 30)
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.RESIZABLE)
        pygame.display.set_caption(self.screen_name)
        pygame.display.set_icon(pygame.image.load('images/icon.png'))

    def update(self):
        self.g.update()

    # Можно каждому ноду сопоставить pygame.surface уже заранее отрисованный. (рисовать через pygame.surface.blit)
    # Я не знаю где их можно хранить, когда ноды добавляются/убираются.
    # Пускай я просто реализую через pygame.draw
    def draw_node(self, n: graph.Node):
        center = self.c.graph_to_pix(n.point)
        # pygame.draw.circle(screen, bg_color, center, node_radius)
        pygame.draw.circle(self.screen, node_color, center, node_radius, node_circle_width)

        # text = arial_font.render(str(n.node_id), False, node_color)
        # screen.blit(text, (center[0] - node_radius // 2, center[1] - node_radius))

    def draw_edge(self, u_id, v_id):
        pos1 = self.c.graph_to_pix(self.g.nodes[u_id].point)
        pos2 = self.c.graph_to_pix(self.g.nodes[v_id].point)
        pygame.draw.line(self.screen, node_color, pos1, pos2, node_circle_width)

    def draw(self):
        self.screen.fill(bg_color)

        # сначала рёбра, потом вершины
        for u_id in g.nodes.keys():
            for v_id in g.edges[u_id].keys():
                if v_id > u_id: self.draw_edge(u_id, v_id)

        for node in g.nodes.values():
            self.draw_node(node)

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
                                g.random_shuffle()
                    case pygame.MOUSEBUTTONDOWN:
                        pass
                    case pygame.MOUSEWHEEL:
                        # поворот вперед
                        self.c.scaling(pygame.mouse.get_pos(), event.y)

if __name__ == '__main__':
    # g = graph.generate_graph(10, 12)
    g = graph.generate_graph(15, 15)
    v = Visualiser(g)
    v.run()
