from typing import List, Dict


def duplicate_search(input: List[int]) -> int | None:
    # using a dict not a set because we only developed proofs for a dict in class
    seen: Dict[int, bool] = {}
    for num in input:
        if num in seen:
            return num
        seen[num] = 1
    return None
