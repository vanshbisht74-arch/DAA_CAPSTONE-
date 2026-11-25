from typing import Dict, List, Tuple

def nearest_neighbor_tsp(dist_matrix: Dict[str, Dict[str, float]], start_node: str = "Depot") -> Tuple[List[str], float]:
    unvisited = set(dist_matrix.keys())
    if start_node not in unvisited:
        return [start_node], 0.0

    tour = [start_node]
    unvisited.remove(start_node)
    curr = start_node
    total_cost = 0.0

    while unvisited:
        next_node = min(unvisited, key=lambda node: dist_matrix[curr].get(node, float('inf')))
        cost = dist_matrix[curr][next_node]
        if cost == float('inf'):
            break
        total_cost += cost
        tour.append(next_node)
        unvisited.remove(next_node)
        curr = next_node

    return_cost = dist_matrix[curr].get(start_node, 0.0)
    total_cost += return_cost
    tour.append(start_node)

    return tour, total_cost
