import numpy as np
import networkx as nx
from scipy.stats import entropy

def effective_information(G):
    """
    Calculates the Effective Information (EI) of a network G.
    EI = Determinism - Degeneracy
    """
    n = G.number_of_nodes()
    if n == 0: return 0

    # Transition Matrix (Row-normalized)
    A = nx.adjacency_matrix(G).toarray()
    out_degree = A.sum(axis=1)

    # Handle sink nodes (avoid divide by zero)
    with np.errstate(divide='ignore', invalid='ignore'):
        W = A / out_degree[:, None]
        W = np.nan_to_num(W) # Sinks stay sinks

    # Effect of Uniform Intervention (Do-Operator)
    # Input distribution is MaxEnt (uniform) -> p(do(x)) = 1/n
    # Output distribution p_eff = (1/n) * sum(W)
    p_eff = W.mean(axis=0)

    # Entropy of the effect distribution (H(Y | do(X~Uniform)))
    H_eff = entropy(p_eff, base=2)

    # Average Entropy of rows (Noise)
    # <H(Y | do(x))>
    H_noise = 0
    for row in W:
        if row.sum() > 0:
            H_noise += entropy(row, base=2)
    H_noise /= n

    # EI = H_eff - H_noise
    return H_eff - H_noise

def causal_beta(G_fine, G_coarse, lambda_ratio):
    """
    Calculates the Causal Beta Function between two scales.
    beta_C = d(EI) / d(ln lambda)
    """
    ei_fine = effective_information(G_fine)
    ei_coarse = effective_information(G_coarse)

    # Logarithmic scaling
    d_ln_lambda = np.log(lambda_ratio)

    beta = (ei_coarse - ei_fine) / d_ln_lambda
    return beta, ei_fine, ei_coarse
