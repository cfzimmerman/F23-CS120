from asyncio import base_tasks
import math
import time
import random
import time
from collections import deque
from typing import List, TypedDict, Dict, Tuple, Any, Deque

"""
See below for mergeSort and countSort functions, and for a useful helper function.
In order to run your experiments, you may find the functions random.randint() and time.time() useful.

In general, for each value of n and each universe size 'U' you will want to
    1. Generate a random array of length n whose keys are in 0, ..., U - 1
    2. Run count sort, merge sort, and radix sort ~10 times each,
       averaging the runtimes of each function.
       (If you are finding that your code is taking too long to run with 10 repitions, you should feel free to decrease that number)

To graph, you can use a library like matplotlib or simply put your data in a Google/Excel sheet.
A great resource for all your (current and future) graphing needs is the Python Graph Gallery
"""


def merge(arr1, arr2):
    sortedArr = []

    i = 0
    j = 0
    while i < len(arr1) or j < len(arr2):
        if i >= len(arr1):
            sortedArr.append(arr2[j])
            j += 1
        elif j >= len(arr2):
            sortedArr.append(arr1[i])
            i += 1
        elif arr1[i][0] <= arr2[j][0]:
            sortedArr.append(arr1[i])
            i += 1
        else:
            sortedArr.append(arr2[j])
            j += 1

    return sortedArr


def mergeSort(arr):
    if len(arr) < 2:
        return arr

    midpt = int(math.ceil(len(arr) / 2))

    half1 = mergeSort(arr[0:midpt])
    half2 = mergeSort(arr[midpt:])

    return merge(half1, half2)


def countSort(univsize, arr):
    universe = []
    for i in range(univsize):
        universe.append([])

    for elt in arr:
        universe[elt[0]].append(elt)

    sortedArr = []
    for lst in universe:
        for elt in lst:
            sortedArr.append(elt)

    return sortedArr


def BC(n, b, k) -> List[int]:
    if b < 2:
        raise ValueError()
    digits = []
    for i in range(k):
        digits.append(n % b)
        n = n // b
    if n > 0:
        raise ValueError()
    return digits


def bcFaster(num: int, base: int, k: int) -> int:
    if base < 2:
        raise ValueError()
    digits = []
    for i in range(k):
        digits.append(num % base)
        num = num // base
    if num > 0:
        raise ValueError()

    res: int = 0
    mult: int = 1
    for digit in digits:
        res += digit * mult
        mult *= 10
    return res


"""
class InputSortable(TypedDict):
    k: int
    v: int
"""

InputSortable = Tuple[int, Any]

RadixSortable = Tuple[int, InputSortable]


"""
def radixSort(
    univsize: int, base: int, arr: List[InputSortable]
) -> List[InputSortable]:
    numDigits: int = math.ceil(math.log(univsize) / math.log(base))
    inputLen = len(arr)
    radixSortables: List[RadixSortable] = [None] * inputLen
    for ind, entry in enumerate(arr):
        radixSortables[ind] = (bcFaster(entry[0], base, numDigits), entry)

    for digit in range(0, numDigits):
        for ind, entry in enumerate(countSort(univsize, radixSortables)):
            radixSortables[ind] = (entry[0] // 10, entry[1])

    for ind, entry in enumerate(radixSortables):
        arr[ind] = entry[1]
    return arr
"""


def radixSort(
    univsize: int, base: int, arr: List[InputSortable]
) -> List[InputSortable]:
    numDigits: int = math.ceil(math.log(univsize) / math.log(base))
    inputLen = len(arr)
    radixSortables: List[RadixSortable] = [(0, "")] * inputLen
    for digit in range(0, numDigits):
        for ind in range(0, inputLen):
            radixSortables[ind] = (BC(arr[ind][0], base, numDigits)[digit], arr[ind])
        for ind, entry in enumerate(countSort(univsize, radixSortables)):
            arr[ind] = entry[1]
    return arr


def genTestArr(ct: int, maxNum: int) -> List[InputSortable]:
    res: List[InputSortable] = []
    for _ in range(0, ct):
        res.append((int(random.random() * maxNum), "T"))
    return res


def runTest(ct: int) -> List[InputSortable]:
    univSize = 1000
    base = 2
    arr: List[InputSortable] = genTestArr(ct, univSize)
    out = radixSort(univSize, base, arr)
    prev: int = -math.inf
    for entry in out:
        assert prev <= entry[0]
        prev = entry[0]
    return arr


def clock(ct: int) -> int:
    start = time.time()
    numTests = 20
    for _ in range(0, numTests):
        runTest(ct)
    return (time.time() - start) / numTests


# res = runTest(10)
# print(res)

# print(clock(50_000))

# print(BC(num, base, k))
# print(bcFaster(num, base, k))
