from dataclasses import dataclass
from typing import Dict, List, Tuple

@dataclass
class Parcel:
    id: str
    weight: int
    value: int
    deadline: int
    destination: str

class RoadGraph:
    def __init__(self):
        self.adj: Dict[str, List[Tuple[str, float]]] = {}

    def add_edge(self, u: str, v: str, weight: float):
        if u not in self.adj:
            self.adj[u] = []
        if v not in self.adj:
            self.adj[v] = []
        self.adj[u].append((v, weight))
        self.adj[v].append((u, weight))

    def get_nodes(self) -> List[str]:
        return list(self.adj.keys())
