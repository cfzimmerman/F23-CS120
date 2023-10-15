from ps4 import QuickSelect
from typing import List, Tuple
from random import random
from math import floor

KV = Tuple[int, int]


def get_rand_inputs(ct: int) -> List[KV]:
    output: List[KV] = []
    for _ in range(0, ct):
        output.append((floor(random() * ct), 0))
    return output


def test_qs(ct: int, k: int) -> KV:
    arr = get_rand_inputs(ct)
    output = QuickSelect(arr, k)
    arr.sort()
    assert output[0] == arr[k][0]
    return output


n = 100_000
for _ in range(0, 10):
    print(test_qs(n, n // 2))
