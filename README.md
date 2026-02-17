# zoverions-crg

**Causal Renormalization Group for Cosmic Complexity**
*The official computational implementation of "The Recursive Universe" (Zoverions Protocol, Feb 2026)*

```bash
pip install git+https://github.com/zoverions/zoverions-crg.git
```

**What it does**
Takes any graph (neural net, city grid, galaxy cluster, scale-free network…) and computes:
- **Effective Information** EI(λ) at any coarse-graining scale (operationalizes Lemma 1)
- **Causal Beta Function** β_C(λ) = dEI/d ln λ
- Automatic classification: Reductionist (β_C < 0), Emergent (β_C > 0), Resurgence (second positive regime)

Exactly as defined in Sections II–IV of the paper.

### Quick Start

```python
from zoverions_crg.core_logic import causal_beta_flow, classify_flow
import networkx as nx

G = nx.scale_free_graph(500)          # your system
scales = [1.0, 2.0, 5.0, 10.0]        # coarse-graining factors

beta_values, ei_values = causal_beta_flow(G, scales)
classification = classify_flow(beta_values)

print(f"System type: {classification}")   # "Class III: Causal Emergence (Resurgence)"
```

### Key Features

- Markov-chain proxy for EI(λ) using max-entropy interventions (matches Hoel et al. 2013)
- Hierarchical coarse-graining via Louvain + block-model contraction
- Full renormalization sweep → plot β_C(λ) exactly like Figure 1
- Built-in DESI-style spin-chirality notebook (load your catalog, see 200 Mpc resurgence)
- Zero dependencies beyond `networkx`, `numpy`, `scipy`

### Citation

```bibtex
@misc{zoverions2026,
  title = {The Recursive Universe: A Renormalization Framework for Cosmic Complexity},
  author = {Zoverions Protocol},
  year = {2026},
  howpublished = {\url{https://github.com/zoverions/zoverions-crg}},
  note = {CRG package implements Sections II–IV}
}
```

**Run the code. See the resurgence.**
No screenshots. No philosophy. Just `β_C > 0` at astrophysical scales.
