import numpy as np
import random


node_mass = 1
node_update_delta_t = 1
antigravity_force_const = -1
spring_delta_weight_len = 10
spring_start_len = 0
spring_standard_length_restoring_constant = 0.00001
spring_standard_length = 10
generate_graph_max_x = 100
generate_max_edge_weight = 10
generate_max_nodes_count = 20
generate_max_edges_count_to_nodes_count = 2
generate_max_divider_if_max_edges_count_is_min = 3


def spring_length(weight):
    return spring_delta_weight_len * weight + spring_start_len


def spring_restoring_const(length):
    return spring_standard_length_restoring_constant  # * spring_standard_length / length


class Node:
    def __init__(self, node_id, x="", y=""):
        if x == "": x = random.random() * generate_graph_max_x * 2 - generate_graph_max_x
        if y == "": y = random.random() * generate_graph_max_x * 2 - generate_graph_max_x
        self.node_id = node_id
        self.point = np.array([x, y])
        self.force = np.array([0.0, 0.0])
        self.velocity = np.array([0.0, 0.0])

    def update(self):
        if np.isnan(self.point[0]):
            print("HEY")
        self.velocity += self.force * node_update_delta_t / node_mass
        self.point += self.velocity * node_update_delta_t
        if np.isnan(self.point[0]):
            print("HEY")
        self.force = np.array([0.0, 0.0])

    def shuffle(self):
        self.point = np.array([random.random() * generate_graph_max_x * 2 - generate_graph_max_x,
                               random.random() * generate_graph_max_x * 2 - generate_graph_max_x])


class Graph:
    def __init__(self):
        self.nodes = dict()  # id -> Node
        self.edges = dict()  # u_id -> dict(): v_id -> weight
        self.edges_count = 0

    def add_node(self, node):
        self.nodes[node.node_id] = node
        self.edges[node.node_id] = dict()

    def add_edge(self, u_id, v_id, weight):
        self.edges[u_id][v_id] = weight
        self.edges[v_id][u_id] = weight
        self.edges_count += 1

    def anti_gravity_update(self):
        for u_id in self.nodes.keys():  # первая нода действует на вторую
            for v_id in self.nodes.keys():
                if v_id == u_id:
                    continue
                radius_vector = np.subtract(self.nodes[u_id].point, self.nodes[v_id].point)
                distance = np.linalg.norm(radius_vector)
                force_value = antigravity_force_const * node_mass * node_mass / (distance ** 2)
                delta_force = radius_vector / distance * force_value
                self.nodes[v_id].force += delta_force


    # ОЧЕНЬ СИЛЬНО!!!
    def spring_edge_update(self):
        for u_id in self.nodes.keys():  # первая нода действует на вторую
            for v_id in self.edges[u_id].keys():
                weight = self.edges[u_id][v_id]
                length = spring_length(weight)
                radius_vector = np.subtract(self.nodes[u_id].point, self.nodes[v_id].point)
                distance = np.linalg.norm(radius_vector)
                delta_x = distance - length
                if abs(delta_x) > 100:
                    delta_x = np.sign(delta_x) * 100
                delta_force = radius_vector / distance * spring_restoring_const(length) * delta_x
                self.nodes[v_id].force += delta_force

    def update(self):
        # self.anti_gravity_update()
        self.spring_edge_update()
        for node_id in self.nodes.keys():
            self.nodes[node_id].update()

    def random_shuffle(self):
        for node_id in self.nodes.keys():
            self.nodes[node_id].shuffle()

    def generate_node(self):
        last_node_id = 0
        if len(self.nodes) != 0:
            last_node_id = sorted(list(self.nodes.keys()))[-1]
        new_node = Node(last_node_id + 1)
        self.add_node(new_node)

    def generate_edge(self):
        nodes_count = len(self.nodes)
        if self.edges_count == nodes_count * (nodes_count - 1) // 2:
            raise Exception("В графе все рёбра уже созданы.")
        weight = random.random() * generate_max_edge_weight
        random_nodes = random.sample(list(self.nodes.keys()), len(self.nodes.keys()))
        flag_made = False
        for i in range(len(random_nodes)):
            u_id = random_nodes[i]
            for j in range(i + 1, len(random_nodes)):
                v_id = random_nodes[j]
                # Проверяем, есть ли это ребро. Если нет - создаем.
                # self.edges хранит в себе двустороннее ребро
                if v_id not in self.edges[u_id].keys() and u_id not in self.edges[v_id].keys():
                    flag_made = True
                    self.add_edge(u_id, v_id, weight)
                    break
            if flag_made:
                break
        if not flag_made:
            raise Exception("В графе новое ребро не сгенерировано.")


def generate_graph(nodes_count=-1,
                   edges_count=-1):
    if nodes_count == -1:
        nodes_count = int(random.random() * generate_max_nodes_count)
    if edges_count == -1:
        edges_count = min(nodes_count * (nodes_count - 1) // 2,
                          int(nodes_count * generate_max_edges_count_to_nodes_count))
        if edges_count == nodes_count * (nodes_count - 1) // 2:
            divider = random.random() * (generate_max_divider_if_max_edges_count_is_min - 1) + 1
            edges_count = int(edges_count / divider)
    g = Graph()
    for i in range(nodes_count):
        g.generate_node()
    for i in range(edges_count):
        g.generate_edge()
    return g


if __name__ == '__main__':
    g = generate_graph(5, 6)
    print(g.nodes)
    print(g.edges)
