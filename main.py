import sys
from src.planner import CourierPlanner
from src.algorithms.knapsack import print_dp_table

def main():
    print("=" * 65)
    print("      MINI-COURIER PLANNER - DAA CAPSTONE PROTOTYPE      ")
    print("=" * 65)

    parcels_file = "data/sample_parcels.json"
    graph_file = "data/city_graph.json"
    capacity = int(sys.argv[1]) if len(sys.argv) > 1 else 15

    planner = CourierPlanner(parcels_file, graph_file)
    print(f"Loaded {len(planner.parcels)} parcels from '{parcels_file}'")
    print(f"Loaded road network with {len(planner.graph.get_nodes())} nodes from '{graph_file}'")
    print(f"Truck Capacity: {capacity} kg\n")

    result = planner.plan(truck_capacity=capacity)

    print("[Phase 2] Prioritized Parcels (Earliest Deadline First):")
    for p in result["sorted_parcels"]:
        print(f"  - {p.id:<4} Deadline: {p.deadline:>3}m | Weight: {p.weight:>2}kg | Value: {p.value:>2} | Destination: {p.destination}")

    print(f"\n[Phase 2] Knapsack Optimal Box Packing (Capacity: {capacity} kg):")
    print(f"  Total Packed Weight: {result['total_weight']} kg / {capacity} kg")
    print(f"  Total Priority Value: {result['total_value']}")
    print("  Selected Parcels:")
    for p in result["packed_parcels"]:
        print(f"    * {p.id}: {p.weight}kg, Value: {p.value}, Deadline: {p.deadline}m -> Deliver to {p.destination}")

    print("\n[Phase 2 Evidence] Dynamic Programming (0/1 Knapsack) State Table:")
    print_dp_table(result["dp_table"], result["sorted_parcels"], capacity)

    print("\n[Phase 3] Road Network Distance Matrix (Dijkstra):")
    targets = ["Depot"] + result["destinations"]
    header = f"  {'Node':<8}" + "".join(f"{t:>8}" for t in targets)
    print(header)
    for u in targets:
        row = f"  {u:<8}" + "".join(f"{result['dist_matrix'][u][v]:>8.1f}" for v in targets)
        print(row)

    print("\n[Phase 3] Final Delivery Route (Nearest-Neighbor TSP):")
    print("  Route Sequence : " + " -> ".join(result["route"]))
    print(f"  Total Distance : {result['total_distance']:.2f} km")
    print("=" * 65)

if __name__ == "__main__":
    main()
