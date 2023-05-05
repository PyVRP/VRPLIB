from typing import List, TypedDict


class Solution(TypedDict, total=False):
    routes: List[List[int]]
    cost: float
