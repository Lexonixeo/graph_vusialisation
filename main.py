import graph
import visualiser


s = dict()

s["screen_name"] = "Визуализатор графа"
s["start_screen_width"] = 1600
s["start_screen_height"] = 900

s["node_radius"] = 5
s["node_color"] = (255, 255, 255)
s["node_width"] = 5
s["edge_width"] = 5
s["bg_color"] = (0, 0, 0)
s["draw_text"] = False
s["font_name"] = 'Arial'
s["font_size"] = 30

s["start_graph_to_pix_const"] = 1
s["scaling_base"] = 2 ** 0.5

s[""] = ""


if __name__ == '__main__':
    g = graph.generate_graph(15, 15)
    v = visualiser.Visualiser(g, s)
    v.run()