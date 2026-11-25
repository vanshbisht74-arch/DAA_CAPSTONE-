from typing import List
from ..models import Parcel

def merge_sort_parcels(parcels: List[Parcel], key: str = "deadline", reverse: bool = False) -> List[Parcel]:
    if len(parcels) <= 1:
        return parcels

    mid = len(parcels) // 2
    left = merge_sort_parcels(parcels[:mid], key, reverse)
    right = merge_sort_parcels(parcels[mid:], key, reverse)
    return _merge(left, right, key, reverse)

def _merge(left: List[Parcel], right: List[Parcel], key: str, reverse: bool) -> List[Parcel]:
    merged = []
    i = j = 0
    while i < len(left) and j < len(right):
        val_l = getattr(left[i], key)
        val_r = getattr(right[j], key)
        condition = (val_l >= val_r) if reverse else (val_l <= val_r)
        if condition:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged

def quick_sort_parcels(parcels: List[Parcel], key: str = "deadline", reverse: bool = False) -> List[Parcel]:
    arr = list(parcels)
    _quicksort_helper(arr, 0, len(arr) - 1, key, reverse)
    return arr

def _quicksort_helper(arr: List[Parcel], low: int, high: int, key: str, reverse: bool):
    if low < high:
        p = _partition(arr, low, high, key, reverse)
        _quicksort_helper(arr, low, p - 1, key, reverse)
        _quicksort_helper(arr, p + 1, high, key, reverse)

def _partition(arr: List[Parcel], low: int, high: int, key: str, reverse: bool) -> int:
    pivot = getattr(arr[high], key)
    i = low - 1
    for j in range(low, high):
        val = getattr(arr[j], key)
        condition = (val >= pivot) if reverse else (val <= pivot)
        if condition:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1
