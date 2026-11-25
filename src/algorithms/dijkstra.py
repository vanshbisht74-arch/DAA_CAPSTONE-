import heapq
from typing import Dict, List, Tuple
from ..models import RoadGraph

def dijkstra_shortest_path(graph: RoadGraph, start: str) -> Tuple[Dict[str, float], Dict[str, str]]:
    distances = {node: float('inf') for node in graph.get_nodes()}
    predecessors = {node: None for node in graph.get_nodes()}
    distances[start] = 0.0

    pq = [(0.0, start)]
    visited = set()

    while pq:
        curr_dist, u = heapq.heappop(pq)
        if u in visited:
            continue
        visited.add(u)

        for v, weight in graph.adj.get(u, []):
            dist = curr_dist + weight
            if dist < distances[v]:
                distances[v] = dist
                predecessors[v] = u
                heapq.heappush(pq, (dist, v))

    return distances, predecessors

def reconstruct_path(predecessors: Dict[str, str], start: str, target: str) -> List[str]:
    path = []
    curr = target
    while curr is not None:
        path.append(curr)
        if curr == start:
            break
        curr = predecessors.get(curr)
    path.reverse()
    return path if path and path[0] == start else []

def build_distance_matrix(graph: RoadGraph, targets: List[str]) -> Dict[str, Dict[str, float]]:
    matrix = {}
    for node in targets:
        distances, _ = dijkstra_shortest_path(graph, node)
        matrix[node] = {target: distances.get(target, float('inf')) for target in targets}
    return matrix
