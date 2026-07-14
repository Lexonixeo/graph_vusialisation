import numpy as np

import graph


node_mass = 1
# node_update_delta_t = 1


class Point:
    def __init__(self, position, time_now):
        self.position = np.array([position])
        self.velocity = np.array([0.0, 0.0])
        self.mass = node_mass
        self.force = np.array([0.0, 0.0])
        self.last_update_time = time_now

    def update(self, time_now):
        delta_t = time_now - self.last_update_time
        self.velocity += self.force * delta_t / node_mass
        self.position += self.velocity * delta_t
        self.force = np.array([0.0, 0.0])
        self.last_update_time = time_now


class PhysicsEngine:
    def __init__(self, g: graph.Graph):
        self.g = g
