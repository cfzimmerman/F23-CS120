from typing import Tuple, List
from math import floor
from random import random

KV = Tuple[int, int]


def swap(arr: List[KV], ind1: int, ind2: int):
    temp = arr[ind1]
    arr[ind1] = arr[ind2]
    arr[ind2] = temp


def get_pivot(min: int, max: int) -> int:
    return floor((max - min) * random()) + min


def partition(arr: List[KV], left_ind: int, right_ind: int) -> int:
    swap(arr, get_pivot(left_ind, right_ind), right_ind)
    pivot_ind = right_ind
    pivot = arr[right_ind][0]
    right_ind -= 1

    while left_ind <= right_ind:
        while left_ind <= right_ind and pivot < arr[right_ind][0]:
            right_ind -= 1
        while left_ind <= right_ind and arr[left_ind][0] <= pivot:
            left_ind += 1
        if left_ind <= right_ind:
            swap(arr, left_ind, right_ind)
            left_ind += 1
            right_ind -= 1

    swap(arr, pivot_ind, left_ind)
    return left_ind


def run_qs(arr: List[KV], target_ind: int, left: int, right: int) -> KV:
    if left == right:
        return arr[left]
    assert left < right
    pivot_ind = partition(arr, left, right)
    if target_ind < pivot_ind:
        return run_qs(arr, target_ind, left, pivot_ind - 1)
    elif pivot_ind < target_ind:
        return run_qs(arr, target_ind, pivot_ind + 1, right)
    else:
        return arr[pivot_ind]


def quick_select(inputs: List[KV], k: int) -> KV:
    return run_qs(inputs, len(inputs) - k, 0, len(inputs) - 1)


def get_rand_inputs(ct: int) -> List[KV]:
    output: List[KV] = []
    for _ in range(0, ct):
        output.append((floor(random() * ct), 0))
    return output


def test_qs(ct: int, k: int) -> KV:
    arr = get_rand_inputs(ct)
    output = quick_select(arr, k)
    arr.sort()
    assert output[0] == arr[len(arr) - k][0]
    return output


n = 100_000
for _ in range(0, 10):
    print(test_qs(n, n // 2))
