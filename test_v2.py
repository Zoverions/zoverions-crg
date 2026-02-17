from zoverions_crg.core_logic import causal_beta_flow, classify_flow, network_assembly_proxy
import networkx as nx
import numpy as np
import sys

def test_v2_features():
    print("Testing v0.2 features...")

    # Generate random graph
    G = nx.barabasi_albert_graph(200, 3, seed=42)

    # Test network_assembly_proxy
    assembly_index = network_assembly_proxy(G)
    print(f"Network Assembly Index: {assembly_index}")
    assert isinstance(assembly_index, float)

    # Test causal_beta_flow with plot=False
    scales = [1.0, 2.0, 4.0, 8.0]
    beta, ei = causal_beta_flow(G, scale_factors=scales, plot=False)

    print(f"Beta values: {beta}")
    print(f"EI values: {ei}")

    classification = classify_flow(beta)
    print(f"Classification: {classification}")

    # Verify return types and shapes
    assert len(beta) == len(scales) - 1
    assert len(ei) == len(scales) - 1

    print("v0.2 tests passed!")

if __name__ == "__main__":
    try:
        test_v2_features()
    except Exception as e:
        print(f"Test failed: {e}")
        sys.exit(1)
