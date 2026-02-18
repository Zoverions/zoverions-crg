# zoverions_crg/core_logic.py  ← v0.2 (Feb 17 2026)
import networkx as nx
import numpy as np
from scipy.stats import entropy
import matplotlib.pyplot as plt
from typing import List, Tuple, Literal

def transition_matrix(G: nx.Graph) -> np.ndarray:
    A = nx.to_numpy_array(G)
    degrees = np.sum(A, axis=1, dtype=float)
    degrees[degrees == 0] = 1.0
    return A / degrees[:, np.newaxis]

def effective_information(G: nx.Graph, eps: float = 1e-10) -> float:
    """EI(λ) proxy — exactly Lemma 1 + Definition 2"""
    if len(G) < 2:
        return 0.0
    P = transition_matrix(G)
    effect_dist = np.mean(P, axis=0)
    h_effect = entropy(effect_dist + eps)
    h_cond = np.mean([entropy(row + eps) for row in P])
    return float(h_effect - h_cond)

def network_assembly_proxy(G: nx.Graph) -> float:
    """A_N proxy (von Neumann spectral entropy) — full operationalization of Lemma 1"""
    if len(G) < 2: return 0.0
    A = nx.to_numpy_array(G) + 1e-10
    eigvals = np.linalg.eigvalsh(A)
    probs = np.abs(eigvals) / np.sum(np.abs(eigvals))
    return -np.sum(probs * np.log2(probs + 1e-10))

def coarse_grain(G: nx.Graph, target_nodes: int) -> nx.Graph:
    if len(G) <= target_nodes:
        return G.copy()
    try:
        communities = list(nx.community.louvain_communities(G, seed=42))
    except:
        communities = list(nx.community.greedy_modularity_communities(G))
    mapping = {}
    for i, comm in enumerate(communities):
        for node in comm:
            mapping[node] = i
    return nx.quotient_graph(G, communities, relabel=True)

def causal_beta_flow(G_fine: nx.Graph, scale_factors: List[float] = None, plot: bool = True):
    if scale_factors is None:
        scale_factors = [1.0, 2.0, 4.0, 8.0, 16.0, 32.0]

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
    d_ei = np.diff(ei_values)
    d_ln = np.diff(lambda_log)
    beta_values = d_ei / d_ln

    if plot:
        plt.figure(figsize=(11, 6))
        plt.plot(lambda_log[:-1], beta_values, 'o-', lw=3, color='#00ff9d', markersize=8, label='β_C(λ)')
        plt.axhline(0, color='red', ls='--', alpha=0.7)
        plt.xlabel('log₁₀(Scale λ)')
        plt.ylabel('Causal Beta Function β_C(λ)')
        plt.title('Causal Renormalization Flow — Recursive Universe Test')
        plt.grid(True, alpha=0.3)
        plt.legend()
        plt.tight_layout()
        plt.show()

    return beta_values, ei_values[:-1]

def classify_flow(beta_values: np.ndarray, threshold: float = 0.01) -> str:
    mean_beta = np.mean(beta_values)
    if mean_beta < -threshold:
        return "Class I: Reductionist Decay"
    elif abs(mean_beta) < threshold:
        return "Class II: Scale Invariant"
    else:
        if len(beta_values) > 3 and beta_values[-1] > threshold and np.any(beta_values[:-2] < 0):
            return "Class III: Resurgence (Astrophysical)"
        return "Class III: Causal Emergence"
