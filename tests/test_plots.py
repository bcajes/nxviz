"""
Some rudimentary tests. Instantiates a Plot object, but doesn't test plotting.

Discovered that this set of rudimentary tests might be necessary after seeing
the following issue:

    https://github.com/ericmjl/nxviz/issues/160
"""

from .test_utils import diff_plots

from random import random

import networkx as nx

from nxviz import ArcPlot, CircosPlot, GeoPlot, MatrixPlot

from matplotlib.testing.decorators import _image_directories

G = nx.erdos_renyi_graph(n=20, p=0.2)

G_geo = G.copy()
for n, d in G_geo.nodes(data=True):
    G_geo.node[n]['latitude'] = random()
    G_geo.node[n]['longitude'] = random()
    G_geo.node[n]['dpcapacity'] = random()

baseline_dir, result_dir = _image_directories(lambda: 'dummy func')


def test_circos_plot():
    c = CircosPlot(G)  # noqa: F841
    diff = diff_plots(c, "circos.png", baseline_dir, result_dir)
    assert diff is None

def test_matrix_plot():
    m = MatrixPlot(G)  # noqa: F841
    diff = diff_plots(m, "matrix.png", baseline_dir, result_dir)
    assert diff is None

def test_arc_plot():
    a = ArcPlot(G)  # noqa: F841
    diff = diff_plots(a, "arc.png", baseline_dir, result_dir)
    assert diff is None

def test_geo_plot():
    g = GeoPlot(G_geo, node_lat='latitude', node_lon='longitude',  # noqa: F841
                color='dpcapacity')
    diff = diff_plots(g, "geo.png", baseline_dir, result_dir)
    assert diff is None


def test_plot_size():
    c = CircosPlot(G, figsize=(3, 3))  # noqa: F841
    diff = diff_plots(c, "circos33.png", baseline_dir, result_dir)
    assert diff is None

def test_edge_widths():
    # add weight as attribute and fill with random numbers
    edges = G.edges()
    for u, v in edges:
        G[u][v]['weight'] = random()
    # also extract list for testing
    weights = [G[u][v]['weight'] for u, v in edges]
    # add weights as proptery
    c = CircosPlot(G, edge_width="weight")
    assert c.edge_widths == weights
    a = ArcPlot(G, edge_width="weight")
    assert a.edge_widths == weights
    # add weights as list
    c = CircosPlot(G, edge_width=weights)
    assert c.edge_widths == weights
    a = ArcPlot(G, edge_width=weights)
    assert a.edge_widths == weights
