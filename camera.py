import numpy as np


class Camera:
    def __init__(self, settings):
        self.camera_graph_point = [0, 0]
        self.screen_width = settings["start_screen_width"]
        self.screen_height = settings["start_screen_height"]
        self.camera_pix_point = [self.screen_width / 2, self.screen_height / 2]
        self.graph_to_pix_const = settings["start_graph_to_pix_const"]
        self.scaling_base = settings["scaling_base"]

    def update_screen_size(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.camera_pix_point = (self.screen_width / 2, self.screen_height / 2)

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
        coefficient = self.scaling_base ** power
        radius_vector_old = np.array(self.camera_graph_point) - np.array(self.pix_to_graph(mouse_pos))
        radius_vector_new = radius_vector_old * coefficient
        need_to_pan = radius_vector_old - radius_vector_new

        self.graph_to_pix_const *= coefficient
        self.panning(need_to_pan[0], need_to_pan[1])
        # Сохраняем mouse_pos и mouse_graph_pos, панорамируем как-то

    def panning(self, delta_x, delta_y):
        self.camera_graph_point[0] += delta_x
        self.camera_graph_point[1] += delta_y

    def pix_panning(self, delta_pix_x, delta_pix_y):
        self.panning(delta_pix_x / self.graph_to_pix_const, -1 * delta_pix_y / self.graph_to_pix_const)