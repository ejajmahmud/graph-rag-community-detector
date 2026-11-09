"""Core Graph RAG Community Detector implementation."""
from typing import Dict, List, Set, Optional, Tuple, Any


class CommunityCluster:
    def __init__(self, community_id: int, members: List[str], central_hub: str):
        self.community_id = community_id
        self.members = members
        self.central_hub = central_hub


class GraphCommunityDetector:
    def __init__(self):
        self.nodes: Set[str] = set()
        self.edges: Dict[str, Dict[str, float]] = {}  # node -> {neighbor: weight}

    def add_edge(self, u: str, v: str, weight: float = 1.0):
        self.nodes.add(u)
        self.nodes.add(v)
        if u not in self.edges:
            self.edges[u] = {}
        if v not in self.edges:
            self.edges[v] = {}
        self.edges[u][v] = self.edges[u].get(v, 0.0) + weight
        self.edges[v][u] = self.edges[v].get(u, 0.0) + weight

    def detect_communities(self, iterations: int = 5) -> List[CommunityCluster]:
        # Label propagation / modularity clustering
        community_assignment: Dict[str, str] = {node: node for node in self.nodes}

        for _ in range(iterations):
            for node in sorted(list(self.nodes)):
                neighbors = self.edges.get(node, {})
                if not neighbors:
                    continue

                # Tally weights per community label among neighbors
                label_weights: Dict[str, float] = {}
                for neighbor, weight in neighbors.items():
                    n_label = community_assignment[neighbor]
                    label_weights[n_label] = label_weights.get(n_label, 0.0) + weight

                # Adopt dominant neighbor label
                best_label = max(label_weights.items(), key=lambda x: x[1])[0]
                community_assignment[node] = best_label

        # Group by community
        groups: Dict[str, List[str]] = {}
        for node, comm in community_assignment.items():
            if comm not in groups:
                groups[comm] = []
            groups[comm].append(node)

        clusters = []
        for cid, (comm, members) in enumerate(groups.items(), 1):
            # Hub is member with highest internal degree
            hub = max(members, key=lambda n: sum(self.edges.get(n, {}).values()))
            clusters.append(CommunityCluster(cid, members, hub))

        return clusters
