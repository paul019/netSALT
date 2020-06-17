import os
import pickle
import sys

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import yaml

import netsalt
from netsalt import plotting

if len(sys.argv) > 1:
    graph_tpe = sys.argv[-1]
else:
    print("give me a type of graph please!")

params = yaml.full_load(open("graph_params.yaml", "rb"))[graph_tpe]

os.chdir(graph_tpe)

graph = netsalt.load_graph()
netsalt.update_parameters(graph, params)

modes_df = netsalt.load_modes()

mode_competition_matrix = netsalt.load_mode_competition_matrix()

D0_max = 5 * np.max(modes_df["lasing_thresholds"][modes_df["lasing_thresholds"] < 100])
D0_min = 0.8 * np.min(modes_df["lasing_thresholds"])
print(D0_min, D0_max)
n_points = 1000
pump_intensities = np.linspace(D0_min, D0_max, n_points)

modes_df = netsalt.compute_modal_intensities(
    modes_df, pump_intensities, mode_competition_matrix
)

netsalt.save_modes(modes_df)

plotting.plot_ll_curve(graph, modes_df, with_legend=False)

plotting.plot_stem_spectra(graph, modes_df, -1)

plt.show()