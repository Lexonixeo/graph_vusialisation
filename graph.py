import numpy as np
import random

import main
import physics


class Node:
    # may be problem with x: str and y: str, надо :float, :float, но при этом
    # если они не указаны, то рандом.
    def __init__(self, node_id, s: dict, x="", y=""):
        self.generate_graph_max_x = s["generate_graph_max_x"]
        if x == "":
            x = self.get_random_x()
        if y == "":
            y = self.get_random_x()
        self.node_id = node_id
        self.point = physics.Point((x, y), 0, s)

    def get_random_x(self):
        return random.random() * self.generate_graph_max_x * 2 - self.generate_graph_max_x

    def set_position(self, position):
        self.point.position = np.array(position)
        self.point.velocity = np.array([0.0, 0.0])

    def shuffle(self):
        self.set_position([self.get_random_x(), self.get_random_x()])


class Graph:
    def __init__(self, s: dict):
        self.nodes = dict()  # id -> Node
        self.edges = dict()  # u_id -> dict(): v_id -> weight
        self.edges_count = 0
        self.s = s
        self.pe = physics.PhysicsEngine(self, s)

    def add_node(self, node):
        self.nodes[node.node_id] = node
        self.edges[node.node_id] = dict()

    def add_edge(self, u_id, v_id, weight):
        self.edges[u_id][v_id] = weight
        self.edges[v_id][u_id] = weight
        self.edges_count += 1

    def random_shuffle(self):
        for node_id in self.nodes.keys():
            self.nodes[node_id].shuffle()

    def generate_node(self):
        last_node_id = 0
        if len(self.nodes) != 0:
            last_node_id = sorted(list(self.nodes.keys()))[-1]
        new_node = Node(last_node_id + 1, self.s)
        self.add_node(new_node)

    def generate_edge(self):
        nodes_count = len(self.nodes)
        if self.edges_count == nodes_count * (nodes_count - 1) // 2:
            pass
            # raise Exception("В графе все рёбра уже созданы.")
        weight = random.random() * self.s["generate_max_edge_weight"]
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
            pass
            # raise Exception("В графе новое ребро не сгенерировано.")


def generate_graph(s: dict,
                   nodes_count=-1,
                   edges_count=-1):
    if nodes_count == -1:
        nodes_count = int(random.random() * s["generate_max_nodes_count"])
    if edges_count == -1:
        edges_count = min(nodes_count * (nodes_count - 1) // 2,
                          int(nodes_count * s["generate_max_edges_count_to_nodes_count"]))
        if edges_count == nodes_count * (nodes_count - 1) // 2:
            divider = random.random() * (s["generate_max_divider_if_max_edges_count_is_min"] - 1) + 1
            edges_count = int(edges_count / divider)
    g = Graph(s)
    for i in range(nodes_count):
        g.generate_node()
    for i in range(edges_count):
        g.generate_edge()
    return g


if __name__ == '__main__':
    g = generate_graph(main.s, 5, 6)
    print(g.nodes)
    print(g.edges)
