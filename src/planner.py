import json
from typing import Dict, Any, List
from .models import Parcel, RoadGraph
from .algorithms.sorting import merge_sort_parcels
from .algorithms.knapsack import knapsack_01
from .algorithms.dijkstra import build_distance_matrix
from .algorithms.tsp import nearest_neighbor_tsp

class CourierPlanner:
    def __init__(self, parcels_path: str, graph_path: str):
        self.parcels = self._load_parcels(parcels_path)
        self.graph = self._load_graph(graph_path)

    def _load_parcels(self, path: str) -> List[Parcel]:
        with open(path, "r") as f:
            data = json.load(f)
        return [Parcel(**p) for p in data]

    def _load_graph(self, path: str) -> RoadGraph:
        with open(path, "r") as f:
            data = json.load(f)
        graph = RoadGraph()
        for u, v, w in data["edges"]:
            graph.add_edge(u, v, float(w))
        return graph

    def plan(self, truck_capacity: int, sort_key: str = "deadline") -> Dict[str, Any]:
        sorted_parcels = merge_sort_parcels(self.parcels, key=sort_key)
        max_value, packed_parcels, dp_table = knapsack_01(sorted_parcels, truck_capacity)

        destinations = sorted(list(set(p.destination for p in packed_parcels)))
        targets = ["Depot"] + destinations
        dist_matrix = build_distance_matrix(self.graph, targets)

        route, total_distance = nearest_neighbor_tsp(dist_matrix, start_node="Depot")

        return {
            "all_parcels": self.parcels,
            "sorted_parcels": sorted_parcels,
            "packed_parcels": packed_parcels,
            "dp_table": dp_table,
            "total_value": max_value,
            "total_weight": sum(p.weight for p in packed_parcels),
            "destinations": destinations,
            "dist_matrix": dist_matrix,
            "route": route,
            "total_distance": total_distance
        }
