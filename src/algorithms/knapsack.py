from typing import List, Tuple
from ..models import Parcel

def knapsack_01(parcels: List[Parcel], capacity: int) -> Tuple[int, List[Parcel], List[List[int]]]:
    n = len(parcels)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        p = parcels[i - 1]
        for w in range(capacity + 1):
            if p.weight <= w:
                dp[i][w] = max(dp[i - 1][w], dp[i - 1][w - p.weight] + p.value)
            else:
                dp[i][w] = dp[i - 1][w]

    selected = []
    w = capacity
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            selected.append(parcels[i - 1])
            w -= parcels[i - 1].weight

    selected.reverse()
    max_value = dp[n][capacity]
    return max_value, selected, dp

def print_dp_table(dp: List[List[int]], parcels: List[Parcel], capacity: int):
    header = f"{'Item / W':<10}" + "".join(f"{w:>4}" for w in range(capacity + 1))
    print(header)
    print("-" * len(header))
    for i in range(len(dp)):
        label = "0 (init)" if i == 0 else f"{parcels[i - 1].id} (w={parcels[i - 1].weight})"
        row_str = f"{label:<10}" + "".join(f"{dp[i][w]:>4}" for w in range(capacity + 1))
        print(row_str)
