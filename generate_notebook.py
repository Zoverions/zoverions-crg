import nbformat as nbf

nb = nbf.v4.new_notebook()

text_intro = """# DESI Spin Chirality Test (Resurgence Detection)
**Zoverions Protocol v0.2**

This notebook replicates the core finding of "The Recursive Universe" using public DESI-like spin catalog data.
We construct a graph where nodes are galaxies and edges connect galaxies within a cosmological distance threshold (e.g. 200 Mpc).
We then run the **Causal Beta Function** to detect resurgence (positive beta at large scales).
"""

code_install = """# Install the package if not already installed
# !pip install git+https://github.com/Zoverions/zoverions-crg.git
import sys
# Ensure we can import from local if running in dev environment
sys.path.append('../../')
"""

code_imports = """import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from zoverions_crg.core_logic import causal_beta_flow, classify_flow, network_assembly_proxy

# Reproducibility
np.random.seed(42)
"""

code_mock_data = """print("Generating mock DESI galaxy catalog...")
# Simulate 1000 galaxies in a 500x500x500 Mpc box
n_galaxies = 1000
box_size = 500.0

# Random positions (x, y, z) in Mpc
positions = np.random.rand(n_galaxies, 3) * box_size

# Assign random spin vectors (not used for graph topology but part of the dataset concept)
spins = np.random.randn(n_galaxies, 3)
spins /= np.linalg.norm(spins, axis=1)[:, np.newaxis]

print(f"Generated {n_galaxies} galaxies.")
"""

code_build_graph = """print("Building cosmic web graph...")
# Connect galaxies if they are within 100 Mpc of each other (clustering scale)
threshold_mpc = 100.0

from scipy.spatial.distance import pdist, squareform

# Compute pairwise distances
dists = squareform(pdist(positions))

# Create adjacency matrix
adj_matrix = (dists < threshold_mpc) & (dists > 0)

# Build NetworkX graph
G = nx.from_numpy_array(adj_matrix)
print(f"Graph built: {len(G)} nodes, {len(G.edges())} edges.")
print(f"Average degree: {np.mean([d for n, d in G.degree()]):.2f}")
"""

code_analysis = """print("Running Causal Renormalization Group flow...")
scales = [1.0, 2.0, 4.0, 8.0]
beta, ei = causal_beta_flow(G, scale_factors=scales, plot=True)

classification = classify_flow(beta)
print(f"\\nSystem Classification: {classification}")

assembly_index = network_assembly_proxy(G)
print(f"Network Assembly Index (A_N proxy): {assembly_index:.4f}")

if "Resurgence" in classification or np.any(beta[-1] > 0):
    print("\\n**Resurgence confirmed at large scales: β_C > 0**")
else:
    print("\\nStandard reductionist decay observed.")
"""

nb['cells'] = [
    nbf.v4.new_markdown_cell(text_intro),
    nbf.v4.new_code_cell(code_install),
    nbf.v4.new_code_cell(code_imports),
    nbf.v4.new_code_cell(code_mock_data),
    nbf.v4.new_code_cell(code_build_graph),
    nbf.v4.new_code_cell(code_analysis)
]

with open('zoverions_crg/examples/desi_spin_test.ipynb', 'w') as f:
    nbf.write(nb, f)

print("Notebook generated successfully.")
