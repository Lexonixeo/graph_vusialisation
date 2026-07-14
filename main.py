import graph
import visualiser


s = dict()

s["screen_name"] = "Визуализатор графа"
s["start_screen_width"] = 1600
s["start_screen_height"] = 900

s["node_radius"] = 5  # 20
s["node_color"] = (255, 255, 255)
s["node_width"] = 5
s["edge_width"] = 5
s["bg_color"] = (0, 0, 0)
s["draw_text"] = False  # True
s["font_name"] = 'Arial'
s["font_size"] = 30

s["start_graph_to_pix_const"] = 1
s["scaling_base"] = 2 ** 0.5

s["node_mass"] = 1
s["antigravity_force_const"] = -2
s["antigravity_epsilon"] = 0.001
s["spring_delta_weight_len"] = 25
s["spring_start_len"] = 0
s["spring_standard_length_restoring_constant"] = 0.00001
s["spring_standard_length"] = 50
s["friction_const"] = 0.0003  # 0.0003 best
s["friction_normal_reaction_force"] = 1
s["friction_epsilon"] = 0.001

s["generate_graph_max_x"] = 100
s["generate_max_edge_weight"] = 10
s["generate_max_nodes_count"] = 20
s["generate_max_edges_count_to_nodes_count"] = 2
s["generate_max_divider_if_max_edges_count_is_min"] = 3


if __name__ == '__main__':
    g = graph.generate_graph(s, 15, 15)
    v = visualiser.Visualiser(g, s)
    v.run()