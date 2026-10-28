import os
import networkx as nx
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
from sklearn.metrics import adjusted_rand_score, normalized_mutual_info_score
from networkx.algorithms.community.quality import modularity

os.makedirs('figures', exist_ok=True)
os.makedirs('results', exist_ok=True)

# 1. Load Data
edges = []
with open('ucidata-zachary/out.ucidata-zachary', 'r') as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith('%'):
            continue
        parts = line.split()
        edges.append((int(parts[0]), int(parts[1])))

G = nx.Graph()
G.add_edges_from(edges)

# Ground truth from Zachary
zkc = nx.karate_club_graph()
gt = {n + 1: zkc.nodes[n]['club'] for n in zkc.nodes()}

# 2. Fixed layout
pos = nx.spring_layout(G, seed=42, k=0.35)

# 3. Community detection
# Louvain
c_louvain = sorted([sorted(list(c)) for c in nx.community.louvain_communities(G, seed=42)], key=len, reverse=True)
q_louvain = modularity(G, c_louvain)

# LPA
c_lpa = sorted([sorted(list(c)) for c in nx.community.asyn_lpa_communities(G, seed=42)], key=len, reverse=True)
q_lpa = modularity(G, c_lpa)

# Girvan Newman
gn_gen = nx.community.girvan_newman(G)
gn_levels = []
best_gn = None
best_q = -1
for i, communities in enumerate(gn_gen):
    comms = sorted([sorted(list(c)) for c in communities], key=len, reverse=True)
    q = modularity(G, comms)
    gn_levels.append((len(comms), q, comms))
    if q > best_q:
        best_q = q
        best_gn = comms
    if len(comms) >= 10:
        break

# k=2 for GN
gn_k2 = gn_levels[0][2]
q_gn_k2 = gn_levels[0][1]

# 4. Node mapping
node_list = sorted(G.nodes())

def comms_to_map(comms, prefix):
    mapping = {}
    for i, comm in enumerate(comms):
        for node in comm:
            mapping[node] = f"{prefix}_{i+1}"
    return mapping

map_gt = {n: gt[n] for n in node_list}
map_louvain = comms_to_map(c_louvain, "Louvain")
map_lpa = comms_to_map(c_lpa, "LPA")
map_gn_opt = comms_to_map(best_gn, "GN_Opt")
map_gn_k2 = comms_to_map(gn_k2, "GN_k2")

# Summary table
summary_data = [
    {
        "Algorithm": "Ground Truth (Faction)",
        "Num_Communities": 2,
        "Modularity_Q": modularity(G, [[n for n, c in gt.items() if c == 'Mr. Hi'], [n for n, c in gt.items() if c == 'Officer']]),
        "Community_Sizes": str([len([n for n, c in gt.items() if c == 'Mr. Hi']), len([n for n, c in gt.items() if c == 'Officer'])]),
        "ARI_vs_GroundTruth": 1.0000,
        "NMI_vs_GroundTruth": 1.0000
    },
    {
        "Algorithm": "Louvain",
        "Num_Communities": len(c_louvain),
        "Modularity_Q": q_louvain,
        "Community_Sizes": str([len(c) for c in c_louvain]),
        "ARI_vs_GroundTruth": adjusted_rand_score([map_gt[n] for n in node_list], [map_louvain[n] for n in node_list]),
        "NMI_vs_GroundTruth": normalized_mutual_info_score([map_gt[n] for n in node_list], [map_louvain[n] for n in node_list])
    },
    {
        "Algorithm": "Label Propagation (LPA)",
        "Num_Communities": len(c_lpa),
        "Modularity_Q": q_lpa,
        "Community_Sizes": str([len(c) for c in c_lpa]),
        "ARI_vs_GroundTruth": adjusted_rand_score([map_gt[n] for n in node_list], [map_lpa[n] for n in node_list]),
        "NMI_vs_GroundTruth": normalized_mutual_info_score([map_gt[n] for n in node_list], [map_lpa[n] for n in node_list])
    },
    {
        "Algorithm": "Girvan-Newman (Optimal Q)",
        "Num_Communities": len(best_gn),
        "Modularity_Q": best_q,
        "Community_Sizes": str([len(c) for c in best_gn]),
        "ARI_vs_GroundTruth": adjusted_rand_score([map_gt[n] for n in node_list], [map_gn_opt[n] for n in node_list]),
        "NMI_vs_GroundTruth": normalized_mutual_info_score([map_gt[n] for n in node_list], [map_gn_opt[n] for n in node_list])
    },
    {
        "Algorithm": "Girvan-Newman (k=2)",
        "Num_Communities": len(gn_k2),
        "Modularity_Q": q_gn_k2,
        "Community_Sizes": str([len(c) for c in gn_k2]),
        "ARI_vs_GroundTruth": adjusted_rand_score([map_gt[n] for n in node_list], [map_gn_k2[n] for n in node_list]),
        "NMI_vs_GroundTruth": normalized_mutual_info_score([map_gt[n] for n in node_list], [map_gn_k2[n] for n in node_list])
    }
]

df_summary = pd.DataFrame(summary_data)
df_summary.to_csv("results/community_detection_summary.csv", index=False)
print(df_summary.to_string())

