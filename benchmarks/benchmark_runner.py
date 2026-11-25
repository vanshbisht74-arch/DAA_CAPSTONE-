import os
import time
import random
import matplotlib.pyplot as plt
from src.models import Parcel, RoadGraph
from src.algorithms.sorting import merge_sort_parcels, quick_sort_parcels
from src.algorithms.knapsack import knapsack_01
from src.algorithms.dijkstra import dijkstra_shortest_path
from src.algorithms.tsp import nearest_neighbor_tsp

def benchmark_sorting():
    sizes = [100, 500, 1000, 2000, 5000]
    merge_times = []
    quick_times = []

    print("\n--- Benchmarking Sorting (Merge Sort vs Quick Sort) ---")
    print(f"{'Size (N)':<10}{'Merge Sort (s)':<18}{'Quick Sort (s)':<18}")
    for s in sizes:
        parcels = [
            Parcel(f"P{i}", random.randint(1, 20), random.randint(1, 50), random.randint(10, 500), f"C{i % 10}")
            for i in range(s)
        ]

        t0 = time.perf_counter()
        merge_sort_parcels(parcels, key="deadline")
        t_merge = time.perf_counter() - t0
        merge_times.append(t_merge)

        t0 = time.perf_counter()
        quick_sort_parcels(parcels, key="deadline")
        t_quick = time.perf_counter() - t0
        quick_times.append(t_quick)

        print(f"{s:<10}{t_merge:<18.6f}{t_quick:<18.6f}")

    return sizes, merge_times, quick_times

def benchmark_knapsack():
    sizes = [10, 25, 50, 100, 150, 200]
    knapsack_times = []
    capacity = 100

    print("\n--- Benchmarking 0/1 Knapsack DP (Capacity W=100) ---")
    print(f"{'Parcels (N)':<15}{'Runtime (s)':<18}")
    for s in sizes:
        parcels = [
            Parcel(f"P{i}", random.randint(1, 15), random.randint(1, 30), 60, "C1")
            for i in range(s)
        ]

        t0 = time.perf_counter()
        knapsack_01(parcels, capacity)
        t_knap = time.perf_counter() - t0
        knapsack_times.append(t_knap)
        print(f"{s:<15}{t_knap:<18.6f}")

    return sizes, knapsack_times

def benchmark_dijkstra():
    sizes = [10, 30, 60, 100, 200]
    dijkstra_times = []

    print("\n--- Benchmarking Dijkstra Shortest Path ---")
    print(f"{'Vertices (V)':<15}{'Runtime (s)':<18}")
    for s in sizes:
        g = RoadGraph()
        nodes = [f"N{i}" for i in range(s)]
        for i in range(s):
            for _ in range(4):
                target = random.choice(nodes)
                if target != nodes[i]:
                    g.add_edge(nodes[i], target, random.uniform(1.0, 15.0))

        t0 = time.perf_counter()
        dijkstra_shortest_path(g, nodes[0])
        t_dijkstra = time.perf_counter() - t0
        dijkstra_times.append(t_dijkstra)
        print(f"{s:<15}{t_dijkstra:<18.6f}")

    return sizes, dijkstra_times

def generate_plots():
    os.makedirs("benchmarks/plots", exist_ok=True)
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))

    # 1. Sorting
    s_sizes, m_times, q_times = benchmark_sorting()
    axes[0].plot(s_sizes, m_times, marker="o", color="#1f77b4", label="Merge Sort O(N log N)")
    axes[0].plot(s_sizes, q_times, marker="s", color="#d62728", label="Quick Sort O(N log N)")
    axes[0].set_title("Sorting Runtimes", fontsize=12, fontweight="bold")
    axes[0].set_xlabel("Number of Parcels (N)")
    axes[0].set_ylabel("Execution Time (seconds)")
    axes[0].grid(True, linestyle="--", alpha=0.6)
    axes[0].legend()

    # 2. Knapsack DP
    k_sizes, k_times = benchmark_knapsack()
    axes[1].plot(k_sizes, k_times, marker="^", color="#ff7f0e", label="0/1 Knapsack O(N * W)")
    axes[1].set_title("Knapsack DP Runtime (W=100)", fontsize=12, fontweight="bold")
    axes[1].set_xlabel("Number of Parcels (N)")
    axes[1].set_ylabel("Execution Time (seconds)")
    axes[1].grid(True, linestyle="--", alpha=0.6)
    axes[1].legend()

    # 3. Dijkstra
    d_sizes, d_times = benchmark_dijkstra()
    axes[2].plot(d_sizes, d_times, marker="d", color="#2ca02c", label="Dijkstra O((V+E) log V)")
    axes[2].set_title("Dijkstra Shortest Path", fontsize=12, fontweight="bold")
    axes[2].set_xlabel("Number of Vertices (V)")
    axes[2].set_ylabel("Execution Time (seconds)")
    axes[2].grid(True, linestyle="--", alpha=0.6)
    axes[2].legend()

    plt.tight_layout()
    output_path = "benchmarks/plots/runtime_analysis.png"
    plt.savefig(output_path, dpi=300)
    print(f"\n[SUCCESS] Runtime analysis plot saved to '{output_path}'")

if __name__ == "__main__":
    generate_plots()
