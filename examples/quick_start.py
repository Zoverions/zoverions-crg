import networkx as nx
from zoverions_crg.core import causal_beta

# 1. Generate a Micro-Scale Network (e.g., Random Geometric Graph)
G_micro = nx.random_geometric_graph(1000, 0.125)

# 2. Renormalize (Coarse-Grain) to Macro-Scale
# (Simulated clustering logic)
mapping = {node: node // 10 for node in G_micro.nodes()}
G_macro = nx.quotient_graph(G_micro, lambda u, v: mapping[u] == mapping[v], relabel=True)

# 3. Calculate Causal Beta Function
lambda_ratio = 10  # Scale difference
beta, ei_micro, ei_macro = causal_beta(G_micro, G_macro, lambda_ratio)

print(f"Micro EI: {ei_micro:.3f} bits")
print(f"Macro EI: {ei_macro:.3f} bits")
print(f"Causal Beta: {beta:.3f}")

if beta > 0:
    print(">> EMERGENCE DETECTED (Class III)")
elif beta < 0:
    print(">> REDUCTIONIST DECAY (Class I)")
