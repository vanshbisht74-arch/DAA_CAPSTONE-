# Mini-Courier Planner: Intelligent Delivery & Packing Optimization
**Course:** Design & Analysis of Algorithms (ETCCDA302)  
**Programme:** B.Tech CSE & Specializations  
**Institution:** K.R. Mangalam University 
**Student Name:** Vansh Viraj Bisht
**Roll No.:** 2501010183
**Submission Mode:** GitHub / Zosima  

---

## 1. Project Overview & Problem Statement

The **Mini-Courier Planner** is an integrated algorithmic prototype that simulates an automated dispatch system for courier logistics. Given an incoming collection of delivery packages with varying deadlines, weights, priority values, and target destinations, the system:
1. **Prioritizes** parcels by delivery urgency using Divide-and-Conquer Sorting ($O(N \log N)$).
2. **Optimizes Vehicle Packing** under fixed weight capacity constraints using Dynamic Programming (0/1 Knapsack, $\Theta(N \cdot W)$).
3. **Calculates Shortest Road Paths** across the city intersection network using Dijkstra's Algorithm with a priority queue ($O((V + E) \log V)$).
4. **Constructs an Efficient Delivery Route Tour** starting and terminating at the central depot using the Nearest-Neighbor Traveling Salesperson Approximation Heuristic ($O(K^2)$).
5. **Benchmarks Empirical Scalability** against theoretical computational complexities across variable input scales.

---

## 2. University Rubric & Phase Compliance Matrix (100 Marks)

| Phase | Marks | Prescribed Task | Implementation & Deliverables | Status |
|---|:---:|---|---|:---:|
| **Phase 1: Problem Design & Planning** | 20 | Define parcel attributes, graph format, pipeline integration, data schemas. | `src/models.py`, `data/sample_parcels.json`, `data/city_graph.json` | Completed |
| **Phase 2: Prioritization & Box Packing** | 20 | Sort parcels by deadline/priority; apply 0/1 Knapsack DP with table evidence. | `src/algorithms/sorting.py`, `src/algorithms/knapsack.py`, DP table printout | Completed |
| **Phase 3: Route Maker & Graph Processing** | 20 | City road graph, Dijkstra shortest paths, nearest-neighbor TSP tour. | `src/algorithms/dijkstra.py`, `src/algorithms/tsp.py`, distance submatrix | Completed |
| **Phase 4: Performance Testing & Optimization** | 20 | Benchmark with multiple input sizes, plot runtime charts, optimization analysis. | `benchmarks/benchmark_runner.py`, `runtime_analysis.png`, `large_dataset.json` | Completed |
| **Phase 5: Final Report & Demonstration** | 20 | Integrated CLI, output traces, documentation quality, viva defense answers. | `main.py`, `src/planner.py`, `README.md` | Completed |

---

## 3. System Architecture & Workflow

```
[Raw Parcels JSON]  +  [City Road Network JSON]
        │
        ▼ (Phase 1)
[Data Modeling: Parcel & RoadGraph Classes]
        │
        ▼ (Phase 2)
[Divide-and-Conquer Sorting: Merge Sort / Quick Sort]
  ──> Orders parcels by earliest deadline
        │
        ▼ (Phase 2)
[0/1 Knapsack Dynamic Programming]
  ──> Maximizes value under Truck Capacity constraint (W)
  ──> Generates (N+1) x (W+1) DP Table & Backtracks selected parcels
        │
        ▼ (Phase 3)
[Dijkstra's Algorithm (Min-Heap Priority Queue)]
  ──> Determines all-pairs shortest distances between [Depot + Destinations]
        │
        ▼ (Phase 3)
[Nearest-Neighbor TSP Approximation]
  ──> Constructs closed delivery route: Depot -> C2 -> C1 -> C3 -> Depot
        │
        ▼ (Phase 4 & 5)
[Benchmarking Suite & CLI Execution Output]
```

---

## 4. Project Directory Structure

```text
DAA_Capstone/
├── data/
│   ├── sample_parcels.json            # 6 sample parcels with deadlines, weights, values, and destinations
│   ├── city_graph.json               # City road network: 6 nodes, 8 weighted edges
│   └── large_dataset.json            # 20 parcels across 10 destinations for scalability testing
├── src/
│   ├── __init__.py
│   ├── models.py                     # Parcel and RoadGraph data models
│   ├── planner.py                    # Integrated pipeline orchestrator
│   └── algorithms/
│       ├── __init__.py
│       ├── sorting.py                # Merge Sort and Quick Sort implementations
│       ├── knapsack.py               # 0/1 Knapsack DP with table reconstruction and visualizer
│       ├── dijkstra.py               # Min-heap Dijkstra single-source shortest path & distance matrix
│       └── tsp.py                    # Nearest Neighbor TSP heuristic route generator
├── benchmarks/
│   ├── __init__.py
│   ├── benchmark_runner.py           # Empirical runtime profiler across multiple input scales
│   └── plots/
│       └── runtime_analysis.png      # 3-panel runtime comparison chart
├── main.py                           # CLI demonstration runner
├── requirements.txt                  # Python dependencies (matplotlib)
├── IMPLEMENTATION_GUIDE.md           # Implementation blueprint and commit history guide
└── README.md                         # Complete project documentation and viva defense
```

---

## 5. Algorithmic Implementation Details

### 5.1. Parcel Prioritization (Merge Sort & Quick Sort)
- **File:** `src/algorithms/sorting.py`
- Parcels must be sorted by delivery urgency (deadline in minutes).
- **Merge Sort:** Divide-and-conquer strategy recursively splitting the list into halves and merging them in sorted order. Provides a guaranteed worst-case time complexity of $\Theta(N \log N)$ and stable sorting.
- **Quick Sort:** In-place partitioning algorithm selecting the last element as a pivot and partitioning elements smaller/larger than the pivot. Provides average time complexity of $\Theta(N \log N)$ with minimal memory overhead ($O(\log N)$ stack space).

### 5.2. Vehicle Box Packing (0/1 Knapsack Dynamic Programming)
- **File:** `src/algorithms/knapsack.py`
- Courier vehicles have a strict payload weight limit $W$ (default: 15 kg). Parcels are discrete and indivisible (cannot take a fraction of a parcel).
- **Recurrence Relation:**
  $$\text{dp}[i][w] = \begin{cases} \text{dp}[i-1][w] & \text{if } w_i > w \\ \max(\text{dp}[i-1][w],\; \text{dp}[i-1][w - w_i] + v_i) & \text{if } w_i \le w \end{cases}$$
- **Backtracking:** Starting from $\text{dp}[N][W]$, if $\text{dp}[i][w] \ne \text{dp}[i-1][w]$, parcel $i$ is included in the packing trip, and capacity is decremented by $w_i$.
- **Complexity:** Time: $\Theta(N \cdot W)$, Space: $O(N \cdot W)$.

### 5.3. Road Network Shortest Paths (Dijkstra's Algorithm)
- **File:** `src/algorithms/dijkstra.py`
- Computes the shortest driving distance between intersections where road segment lengths are positive ($w(u, v) > 0$).
- Uses a min-heap priority queue (`heapq`) to greedily extract the unvisited vertex with the minimum tentative distance.
- Relaxes all outgoing edges: if $\text{dist}[u] + \text{weight} < \text{dist}[v]$, update $\text{dist}[v]$ and push to heap.
- Generates a compact distance matrix between `Depot` and customer destinations for TSP input.
- **Complexity:** Time: $O((V + E) \log V)$, Space: $O(V + E)$.

### 5.4. Route Optimization (Nearest Neighbor TSP Approximation)
- **File:** `src/algorithms/tsp.py`
- Exact TSP is NP-hard ($O(K!)$ brute-force). For practical courier dispatch, a 2-approximation Nearest Neighbor greedy heuristic is employed.
- Starts at the `Depot`, iteratively transitions to the nearest unvisited delivery point according to the Dijkstra distance matrix, and finally traverses back to the `Depot` to complete the closed tour.
- **Complexity:** Time: $O(K^2)$ where $K$ is the number of delivery stops, Space: $O(K)$.

---

## 6. How to Install and Run

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Run the Integrated Delivery Planner
```bash
python main.py
```
*To test with custom truck capacities (e.g. 20 kg or 30 kg):*
```bash
python main.py 20
```

### Step 3: Run the Empirical Benchmarking Suite
```bash
python -m benchmarks.benchmark_runner
```
*The benchmark script prints the runtime tables and saves the high-resolution visualization to `benchmarks/plots/runtime_analysis.png`.*

---

## 7. Execution Output & Verification Evidence

### 7.1. Terminal Output Trace (`python main.py`)
```text
=================================================================
      MINI-COURIER PLANNER - DAA CAPSTONE PROTOTYPE      
=================================================================
Loaded 6 parcels from 'data/sample_parcels.json'
Loaded road network with 6 nodes from 'data/city_graph.json'
Truck Capacity: 15 kg

[Phase 2] Prioritized Parcels (Earliest Deadline First):
  - P5   Deadline:  20m | Weight:  4kg | Value:  9 | Destination: C1
  - P2   Deadline:  30m | Weight:  8kg | Value: 15 | Destination: C2
  - P3   Deadline:  45m | Weight:  3kg | Value:  7 | Destination: C3
  - P1   Deadline:  60m | Weight:  5kg | Value: 10 | Destination: C1
  - P6   Deadline:  75m | Weight:  7kg | Value: 14 | Destination: C5
  - P4   Deadline:  90m | Weight:  6kg | Value: 12 | Destination: C4

[Phase 2] Knapsack Optimal Box Packing (Capacity: 15 kg):
  Total Packed Weight: 15 kg / 15 kg
  Total Priority Value: 31
  Selected Parcels:
    * P5: 4kg, Value: 9, Deadline: 20m -> Deliver to C1
    * P2: 8kg, Value: 15, Deadline: 30m -> Deliver to C2
    * P3: 3kg, Value: 7, Deadline: 45m -> Deliver to C3

[Phase 2 Evidence] Dynamic Programming (0/1 Knapsack) State Table:
Item / W     0   1   2   3   4   5   6   7   8   9  10  11  12  13  14  15
--------------------------------------------------------------------------
0 (init)     0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0
P5 (w=4)     0   0   0   0   9   9   9   9   9   9   9   9   9   9   9   9
P2 (w=8)     0   0   0   0   9   9   9   9  15  15  15  15  24  24  24  24
P3 (w=3)     0   0   0   7   9   9   9  16  16  16  16  22  24  24  24  31
P1 (w=5)     0   0   0   7   9  10  10  16  17  19  19  22  26  26  26  31
P6 (w=7)     0   0   0   7   9  10  10  16  17  19  21  23  26  26  30  31
P4 (w=6)     0   0   0   7   9  10  12  16  17  19  21  23  26  28  30  31

[Phase 3] Road Network Distance Matrix (Dijkstra):
  Node       Depot      C1      C2      C3
  Depot        0.0     3.5     2.0     8.5
  C1           3.5     0.0     1.5     5.0
  C2           2.0     1.5     0.0     6.5
  C3           8.5     5.0     6.5     0.0

[Phase 3] Final Delivery Route (Nearest-Neighbor TSP):
  Route Sequence : Depot -> C2 -> C1 -> C3 -> Depot
  Total Distance : 17.00 km
=================================================================
```

### 7.2. Benchmark Scaling Trace (`python -m benchmarks.benchmark_runner`)
```text
--- Benchmarking Sorting (Merge Sort vs Quick Sort) ---
Size (N)  Merge Sort (s)    Quick Sort (s)    
100       0.000287          0.000140          
500       0.001767          0.001048          
1000      0.002647          0.001459          
2000      0.005740          0.003362          
5000      0.016489          0.011101          

--- Benchmarking 0/1 Knapsack DP (Capacity W=100) ---
Parcels (N)    Runtime (s)       
10             0.000144          
25             0.000324          
50             0.000665          
100            0.001356          
150            0.002044          
200            0.002710          

--- Benchmarking Dijkstra Shortest Path ---
Vertices (V)   Runtime (s)       
10             0.000038          
30             0.000051          
60             0.000110          
100            0.000324          
200            0.000450          

[SUCCESS] Runtime analysis plot saved to 'benchmarks/plots/runtime_analysis.png'
```

---

## 8. Theoretical vs. Empirical Complexity Analysis

| Algorithm | Paradigm | Best Case | Average Case | Worst Case | Space Complexity | Empirical Observation |
|---|---|:---:|:---:|:---:|:---:|---|
| **Merge Sort** | Divide & Conquer | $\Theta(N \log N)$ | $\Theta(N \log N)$ | $O(N \log N)$ | $O(N)$ | Strictly sub-quadratic; predictable runtime regardless of input order. |
| **Quick Sort** | Divide & Conquer | $\Omega(N \log N)$ | $\Theta(N \log N)$ | $O(N^2)$ | $O(\log N)$ | Consistently faster constants than Merge Sort due to cache locality. |
| **0/1 Knapsack** | Dynamic Programming | $\Theta(N \cdot W)$ | $\Theta(N \cdot W)$ | $\Theta(N \cdot W)$ | $O(N \cdot W)$ | Execution time scales strictly linearly with parcel count $N$ for fixed capacity $W$. |
| **Dijkstra** | Greedy / Graph | $O((V+E)\log V)$ | $O((V+E)\log V)$ | $O((V+E)\log V)$ | $O(V)$ | Sub-millisecond execution even with $V=200$ due to binary min-heap efficiency. |
| **Nearest Neighbor** | Approximation Heuristic | $O(K^2)$ | $O(K^2)$ | $O(K^2)$ | $O(K)$ | Instantly resolves vehicle tour without factorial explosion ($O(K!)$). |

---

## 9. Future Optimization Suggestions (Phase 4 Rubric)

1. **Space-Optimized Knapsack:** The DP table space can be reduced from $O(N \cdot W)$ to $O(W)$ using a 1D rolling array traversed backwards if only the maximum value is required, or bitset masking for compact item tracking.
2. **2-Opt Local Search for TSP:** The Nearest-Neighbor heuristic can sometimes produce crossing paths. Implementing a 2-Opt edge swap post-processing pass can eliminate path intersections and reduce total distance by 5–12%.
3. **Multi-Vehicle Fleet Routing (VRP):** Expand the single-truck knapsack model to multiple vehicles using cluster-first, route-second heuristics to distribute parcels across a fleet simultaneously.
4. **Bidirectional or Contraction Hierarchies Dijkstra:** For city graphs with hundreds of thousands of street segments, preprocessing road hierarchies can reduce shortest-path lookup from milliseconds to microseconds.

---

## 10. Viva / Demonstration Defense Guide

### Q1: Why can't we use a Greedy approach for parcel box packing?
> **Answer:** The Greedy method (sorting by value-to-weight ratio) only yields optimal solutions for the **Fractional Knapsack** problem where items can be cut. For indivisible 0/1 parcels, taking the highest ratio item can leave unused weight capacity that prevents taking a combination of items with higher overall value. Dynamic Programming evaluates all sub-capacities, guaranteeing global optimality.

### Q2: Why choose Dijkstra over Bellman-Ford or Floyd-Warshall?
> **Answer:** Road distances between real physical locations are strictly non-negative ($w \ge 0$). Dijkstra runs in $O((V + E) \log V)$ using a min-heap, whereas Bellman-Ford takes $O(V \cdot E)$ (needed only when negative edges exist), and Floyd-Warshall takes $O(V^3)$ (prohibitive for large city maps).

### Q3: How does the system handle an unseen dataset during evaluation?
> **Answer:** The system is fully decoupled from static data. By passing any new JSON file path into `CourierPlanner("new_parcels.json", "new_graph.json")`, the parsing, graph adjacency construction, sorting, DP table generation, and routing compute dynamically on the fly.

### Q4: Trace how Dijkstra found `Depot -> C1 = 3.5` instead of `4.0`.
> **Answer:** The city graph has a direct edge `Depot -> C1` of length `4.0`. However, the path `Depot -> C2` is `2.0`, and the edge `C2 -> C1` is `1.5`. When relaxing the outgoing edges of `C2`, $\text{dist}[\text{Depot} \rightarrow \text{C2}] + \text{weight}(\text{C2}, \text{C1}) = 2.0 + 1.5 = 3.5 < 4.0$. Dijkstra updates the distance of `C1` to `3.5` and sets the predecessor of `C1` to `C2`.
