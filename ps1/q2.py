from typing import List


def bC(n: int, b: int, k: int) -> None | List[int]:
    if b < 2:
        return None
    cArr: List[int] = [0] * k
    for i in range(0, k):
        cI = n % b
        n = (n - cI) / b
        cArr[i] = int(cI)
    if n == 0:
        return cArr
    return None


def powSum(b: int, cArr: List[int]) -> int:
    """Sums the power-adjusted members of the list"""
    pow = 0
    sum = 0
    for ind in range(0, len(cArr)):
        sum += cArr[ind] * (b**pow)
        pow += 1
    return sum


def runTests(n: int, b: int, k: int) -> List[int]:
    cArr = bC(n, b, k)
    if cArr is not None:
        sum = powSum(b, cArr)
        # print(sum)
        assert sum == n
    return cArr


n = 19
cArr = runTests(n=n, b=2, k=8)
print(f"{n}:", cArr)
