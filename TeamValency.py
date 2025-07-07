import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import networkx as nx

# ---------------------
# 1. DEFINE TEAM + MATRIX
# ---------------------
# Editable section: define team members and collaboration scores
team_members = ['Eli', 'Sam', 'Manuel', 'Julia', 'Elena', 'Alex', 'Lisa', 'Michael']

# Each row is how one person rates their collaboration with the others (0–3)
valency_data = {
    "Eli":  [0, 3, 2, 3, 1, 1, 2, 1],
    "Sam":    [2, 0, 1, 2, 2, 2, 1, 0],
    "Manuel": [1, 2, 0, 3, 1, 3, 1, 1],
    "Julia":   [0, 1, 2, 0, 3, 3, 2, 3],
    "Elena":  [2, 1, 1, 1, 0, 3, 1, 1],
    "Alex":  [2, 1, 1, 1, 2, 0, 2, 1],
    "Lisa":  [2, 1, 1, 1, 1, 2, 0, 1],
    "Michael":  [2, 1, 1, 1, 1, 2, 1, 0]
}

valency_matrix = pd.DataFrame(valency_data, index=team_members)

# ---------------------
# 2. PLOT HEATMAP
# ---------------------
plt.figure(figsize=(8, 6))
sns.heatmap(valency_matrix, annot=True, cmap="YlGnBu", linewidths=0.5, fmt='d')
plt.title("Valency Matrix (Perceived Collaboration)")
plt.tight_layout()
plt.savefig("valency_heatmap.png")
plt.show()

# ---------------------
# 3. PLOT NETWORK GRAPH
# ---------------------
# Build directed graph
G = nx.DiGraph()
total_valency = valency_matrix.sum(axis=0) + valency_matrix.sum(axis=1)
for member in valency_matrix.columns:
    G.add_node(member, size=total_valency[member])

for i in valency_matrix.index:
    for j in valency_matrix.columns:
        weight = valency_matrix.loc[i, j]
        if weight > 0:
            G.add_edge(i, j, weight=weight)

# Draw graph
pos = nx.spring_layout(G, seed=42)
plt.figure(figsize=(10, 8))
node_sizes = [G.nodes[n]['size'] * 100 for n in G.nodes]
nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color='lightblue', edgecolors='black')
edge_widths = [G[u][v]['weight'] for u, v in G.edges()]
nx.draw_networkx_edges(G, pos, edgelist=G.edges(), width=edge_widths, alpha=0.7, arrows=True)
nx.draw_networkx_labels(G, pos, font_size=10)
plt.title("Team Valency Network Graph")
plt.axis('off')
plt.tight_layout()
plt.savefig("valency_network_graph.png")
plt.show()
