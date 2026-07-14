import numpy as np

import graph


class Point:
    def __init__(self, position, time_now, s: dict):
        self.position = np.array(position)
        self.velocity = np.array([0.0, 0.0])
        self.mass = s["node_mass"]
        self.force = np.array([0.0, 0.0])
        self.last_update_time = time_now

    def update(self, time_now):
        # сначала v потом x - https://www.youtube.com/watch?v=nCg3aXn5F3M
        delta_t = time_now - self.last_update_time
        self.velocity += self.force * delta_t / self.mass
        self.position += self.velocity * delta_t
        self.force = np.array([0.0, 0.0])
        self.last_update_time = time_now


def spring(edge_weight, s: dict) -> dict:
    d = dict()
    d["length"] = s["spring_delta_weight_len"] * edge_weight + s["spring_start_len"]
    d["restoring_const"] = (s["spring_standard_length_restoring_constant"]
                            # * s["spring_standard_length"] / d["length"]
                            )
    return d


# class Spring:
#     def __init__(self, edge_weight, s: dict):
#         self.length = s["spring_delta_weight_len"] * edge_weight + s["spring_start_len"]
#         self.restoring_const = (s["spring_standard_length_restoring_constant"]
#                                 # * s["spring_standard_length"] / self.length
#                                 )


class PhysicsEngine:
    def __init__(self, g: graph.Graph, s: dict):
        self.g = g
        self.s = s

    def antigravity_update(self):
        for u_id in self.g.nodes.keys():  # первая нода действует на вторую
            for v_id in self.g.nodes.keys():
                if v_id == u_id:
                    continue
                up = self.g.nodes[u_id].point
                vp = self.g.nodes[v_id].point
                radius_vector = np.subtract(up.position, vp.position)
                distance = np.linalg.norm(radius_vector)
                force_value = (self.s["antigravity_force_const"] * up.mass * vp.mass
                               / (distance ** 2 + self.s["antigravity_epsilon"]))  # gemini: + epsilon
                delta_force = radius_vector / distance * force_value
                vp.force += delta_force

    def spring_edge_update(self):
        for u_id in self.g.nodes.keys():  # первая нода действует на вторую
            for v_id in self.g.edges[u_id].keys():
                up = self.g.nodes[u_id].point
                vp = self.g.nodes[v_id].point
                weight = self.g.edges[u_id][v_id]
                length = spring(weight, self.s)["length"]
                radius_vector = np.subtract(up.position, vp.position)
                distance = np.linalg.norm(radius_vector)
                delta_x = distance - length
                # commented т.к. было попыткой исправить баг с улётом вершин в одну сторону
                # проблема была в другом
                # if abs(delta_x) > 100:
                #     delta_x = np.sign(delta_x) * 100
                delta_force = radius_vector / distance * spring(weight, self.s)["restoring_const"] * delta_x
                vp.force += delta_force

    # Сила трения, чтобы убрать энергию
    def friction_update(self):
        for u_id in self.g.nodes.keys():
            up = self.g.nodes[u_id].point
            friction_force = self.s["friction_const"] * self.s["friction_normal_reaction_force"]
            # if np.all(up.velocity == 0):  # gemini порекомендовал сделать не проверку == 0
            if np.linalg.norm(up.velocity) < self.s["friction_epsilon"]:  # а проверку |velocity| < epsilon
                up.velocity = np.array([0.0, 0.0])
                force_value = np.linalg.norm(up.force)
                if force_value <= friction_force:
                    up.force -= up.force
                else:
                    up.force -= up.force / force_value * friction_force
            else:
                velocity_radius_vector = up.velocity / np.linalg.norm(up.velocity)
                up.force += -1 * velocity_radius_vector * friction_force

    def update(self, time_now):
        self.antigravity_update()
        self.spring_edge_update()
        # отталкивание от ребер?
        # отталкивание пересечений рёбер?
        # притяжение к центру?
        # отталкивание от границ?
        # при необходимости воздействие случайной силы на вершину?
        self.friction_update()
        for node_id in self.g.nodes.keys():
            self.g.nodes[node_id].point.update(time_now)