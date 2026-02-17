"""
zoverions_crg.core_logic
Core implementation of the Causal Renormalization Group (CRG)
from "The Recursive Universe" (Zoverions Protocol, Feb 2026)
"""

import networkx as nx
import numpy as np
from scipy.stats import entropy
import matplotlib.pyplot as plt
from typing import List, Tuple, Literal

def transition_matrix(G: nx.Graph) -> np.ndarray:
    """Random-walk transition matrix (undirected → symmetric)."""
    A = nx.to_numpy_array(G)
    degrees = np.sum(A, axis=1, dtype=float)
    degrees[degrees == 0] = 1.0
    return A / degrees[:, np.newaxis]

def effective_information(G: nx.Graph, eps: float = 1e-10) -> float:
    """
    Operational proxy for Effective Information EI(λ)
    (Lemma 1 + Definition 2)
    Max-ent intervention → mutual information I(Do; next)
    """
    if len(G) == 0:
        return 0.0
    P = transition_matrix(G)
    # Effect distribution under uniform intervention
    effect_dist = np.mean(P, axis=0)
    h_effect = entropy(effect_dist + eps)
    # Conditional entropy H(next | do)
    h_cond = np.mean([entropy(row + eps) for row in P])
    return float(h_effect - h_cond)

def coarse_grain(G: nx.Graph, target_nodes: int) -> nx.Graph:
    """Hierarchical coarse-graining via Louvain communities + contraction."""
    if len(G) <= target_nodes:
        return G.copy()
    try:
        communities = list(nx.community.louvain_communities(G, seed=42))
    except:
        communities = list(nx.community.greedy_modularity_communities(G))
    # Contract each community to a supernode
    mapping = {}
    for i, comm in enumerate(communities):
        for node in comm:
            mapping[node] = i
    G_coarse = nx.quotient_graph(G, communities, relabel=True)
    return G_coarse

def causal_beta_flow(G_fine: nx.Graph,
                     scale_factors: List[float] = None,
                     plot: bool = True) -> Tuple[np.ndarray, np.ndarray]:
    """
    Compute β_C(λ) across scales.
    λ ~ log10(number of nodes)  (length scale proxy)
    Returns: beta_values, ei_values
    """
    if scale_factors is None:
        scale_factors = [1.0, 2.0, 4.0, 8.0, 16.0]

    ei_values = []
    node_counts = []
    current_G = G_fine.copy()

    for factor in scale_factors:
        target = max(5, int(len(current_G) / factor))
        current_G = coarse_grain(current_G, target)
        ei = effective_information(current_G)
        ei_values.append(ei)
        node_counts.append(len(current_G))

    ei_values = np.array(ei_values)
    lambda_log = np.log10(np.array(node_counts))
    # Central difference for β_C = dEI / d ln λ ≈ ΔEI / Δlnλ
    d_ei = np.diff(ei_values)
    d_ln_lambda = np.diff(lambda_log)
    beta_values = d_ei / d_ln_lambda

    if plot:
        fig, ax = plt.subplots(figsize=(10, 6))
        # Note: scale_factors[:-1] corresponds to the intervals between steps where beta is defined
        # But here we are plotting against the log of node counts, or similar.
        # The user provided snippet: ax.plot(np.log10([len(G_fine)/f for f in scale_factors[:-1]]), beta_values, ...
        # Let's match the user snippet exactly.
        ax.plot(np.log10([len(G_fine)/f for f in scale_factors[:-1]]), beta_values, 'o-', linewidth=3, color='#00ff9d')
        ax.axhline(0, color='red', linestyle='--', alpha=0.6)
        ax.set_xlabel('log₁₀(Scale λ)')
        ax.set_ylabel('Causal Beta Function β_C(λ)')
        ax.set_title('Causal Renormalization Flow — Resurgence Detected?')
        plt.grid(True, alpha=0.3)
        plt.show()

    return beta_values, ei_values[:-1]  # align lengths

def classify_flow(beta_values: np.ndarray,
                  threshold: float = 0.01) -> Literal["Class I: Reductionist Decay",
                                                       "Class II: Scale Invariant",
                                                       "Class III: Causal Emergence",
                                                       "Class III: Resurgence (Astrophysical)"]:
    """Classify per Section II.C"""
    mean_beta = np.mean(beta_values)
    if mean_beta < -threshold:
        return "Class I: Reductionist Decay"
    elif abs(mean_beta) < threshold:
        return "Class II: Scale Invariant"
    else:
        # Check for resurgence: last regime positive while earlier mixed
        if len(beta_values) > 2 and beta_values[-1] > threshold and np.any(beta_values[:-1] < 0):
            return "Class III: Resurgence (Astrophysical)"
        return "Class III: Causal Emergence"

def network_assembly_proxy(G: nx.Graph) -> float:
    """A_N proxy via von Neumann entropy of adjacency (operationalizes Lemma 1 fully)"""
    if len(G) < 2: return 0.0
    A = nx.to_numpy_array(G)
    eigvals = np.linalg.eigvalsh(A + 1e-10)
    probs = np.abs(eigvals) / np.sum(np.abs(eigvals))
    return -np.sum(probs * np.log2(probs + 1e-10))  # spectral entropy ≈ A_N
