# zoverions-crg: The Causal Renormalization Group

![License](https://img.shields.io/badge/license-MIT-blue.svg) ![Version](https://img.shields.io/badge/version-2.0-green)

**Quantifying the Resurgence of Causal Power at Astrophysical Scales.**

`zoverions-crg` is the open-source implementation of the framework presented in *"The Recursive Universe v2.0"*. It provides tools to calculate Effective Information (EI) and the Causal Beta Function ($\beta_C$) across varying coarse-graining scales.

## The Theory
Standard cosmology assumes complexity peaks at the biological scale and decays into thermodynamic equilibrium.
**We disagree.**

The **Middle-Stack Hypothesis** predicts a **Resurgence** of causal power ($\beta_C > 0$) at astrophysical scales, driven by the network topology of the Cosmic Web.

## Installation
```bash
pip install .

```

## Quick Start: Testing for Resurgence

```python
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

```

## Citation

If you use this code, please cite:

> Zoverions (2026). *The Recursive Universe v2.0: Causal Renormalization and the Infinite Stack.* arXiv:2602.XXXXX.

## License

MIT
