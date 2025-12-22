import matplotlib.pyplot as plt
import networkx as nx

import os, glob
for file in glob.glob('tmp*.png'):
	os.remove(file)

tmp = 0

def draw_edges(cycles:list[list[tuple[int,int,str]]]):
	"""
	draw and save a pretty networkx graph for a list of cycles

	:param cycles: list of cycles (i, j, color)
	"""

	global tmp
	tmp = tmp + 1

	G = nx.Graph()

	for cycle in cycles:
		for (i, j, c) in cycle:
			G.add_edge(str(i), str(j), color=c)

	nx.draw(
		G,
		nx.circular_layout(G),
		with_labels = True,
		edge_color = [G[u][v]['color'] for u, v in G.edges()],
		width = 7.5,
		node_size = 200,
		node_color = 'white',
	)

	plt.savefig(f'tmp{tmp}.png')
	plt.clf()
