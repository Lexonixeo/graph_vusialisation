import pygame

import graph

screen_width = 1600
screen_height = 900
graph_to_pix_const = 3
screen_name = 'Визуализатор графа'
node_radius = 20
node_color = (0, 0, 0)
node_circle_width = 5


camera_pix_point_FIXED = (screen_width / 2, screen_height / 2)


def graph_to_pix(camera_graph_point, graph_point):
    delta_x = graph_point[0] - camera_graph_point[0]
    delta_y = graph_point[1] - camera_graph_point[1]
    delta_pix_x = graph_to_pix_const * delta_x
    delta_pix_y = -1 * graph_to_pix_const * delta_y
    pix_x = camera_pix_point_FIXED[0] + delta_pix_x
    pix_y = camera_pix_point_FIXED[1] + delta_pix_y
    return pix_x, pix_y


# Можно каждому ноду сопоставить pygame.surface уже заранее отрисованный. (рисовать через pygame.surface.blit)
# Я не знаю где их можно хранить, когда ноды добавляются/убираются.
# Пускай я просто реализую через pygame.draw
def draw_node(screen, camera_graph_point, n: graph.Node, font):
    center = graph_to_pix(camera_graph_point, n.point)
    pygame.draw.circle(screen, (255, 255, 255), center, node_radius)
    pygame.draw.circle(screen, (0, 0, 0), center, node_radius, node_circle_width)
    text = font.render(str(n.node_id), False, node_color)
    screen.blit(text, (center[0] - node_radius // 2, center[1] - node_radius))


def draw_edge(screen, camera_graph_point, g: graph.Graph, u_id, v_id):
    pos1 = graph_to_pix(camera_graph_point, g.nodes[u_id].point)
    pos2 = graph_to_pix(camera_graph_point, g.nodes[v_id].point)
    pygame.draw.line(screen, (0, 0, 0), pos1, pos2, node_circle_width)


# рисует одно ребро дважды
def draw_edges(screen, camera_graph_point, g: graph.Graph):
    for u_id in g.nodes.keys():
        for v_id in g.edges[u_id].keys():
            draw_edge(screen, camera_graph_point, g, u_id, v_id)


if __name__ == '__main__':
    g = graph.generate_graph(5, 6)

    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption(screen_name)
    # pygame.display.set_icon(pygame.image.load('images/icon.png'))
    screen.fill((255, 255, 255))

    my_font = pygame.font.SysFont('Arial', 30)

    camera_graph_point = (0, 0)

    flag_running = True
    while flag_running:
        # g.update()

        screen.fill((255, 255, 255))
        draw_edges(screen, camera_graph_point, g)
        for node in g.nodes.values():
            draw_node(screen, camera_graph_point, node, my_font)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                flag_running = False
