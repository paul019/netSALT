import os
import pickle
import sys

import matplotlib.pyplot as plt
import numpy as np
import yaml

import naq_graphs as naq
from naq_graphs import plotting
from graph_generator import generate_pump

if len(sys.argv) > 1:
    graph_tpe = sys.argv[-1]
else:
    print("give me a type of graph please!")

params = yaml.full_load(open("graph_params.yaml", "rb"))[graph_tpe]

os.chdir(graph_tpe)

graph = naq.load_graph()
modes_df = naq.load_modes()

generate_pump(graph_tpe, graph, params)
naq.update_parameters(graph, params)
naq.save_graph(graph)

plotting.plot_naq_graph(graph, edge_colors=params["pump"], node_size=0.1)
plt.savefig("pump_profile.svg")
plt.show()

modes_df = naq.pump_trajectories(modes_df, graph, return_approx=True)
naq.save_modes(modes_df)

qualities = naq.load_qualities()

ax = plotting.plot_scan(
    graph, qualities, modes_df, filename="scan_with_trajectories", relax_upper=True
)
plt.show()
