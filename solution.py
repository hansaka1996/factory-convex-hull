"""
Optimal Patrol Path Around Machines
====================================
Problem:
    Given N axis-aligned rectangles on a factory floor, find the shortest
    simple closed loop that encloses all rectangles.

Approach:
    The optimal path is the convex hull of all rectangle corner points.
    Algorithm: Andrew's Monotone Chain — O(N log N)

Author: SC Printing International
"""

import sys
import math
from typing import List, Tuple

Point = Tuple[float, float]


# ---------------------------------------------------------------------------
# 1. Cross product / orientation test
# ---------------------------------------------------------------------------
def cross(O: Point, A: Point, B: Point) -> float:
    """
    Signed cross product of vectors OA and OB.

    Formula:
        cross(O, A, B) = (A.x - O.x) * (B.y - O.y)
                       - (A.y - O.y) * (B.x - O.x)

    Returns:
        > 0  → counter-clockwise turn (B is left of ray O→A)
        = 0  → O, A, B are collinear
        < 0  → clockwise turn (B is right of ray O→A)
    """
    return (A[0] - O[0]) * (B[1] - O[1]) - (A[1] - O[1]) * (B[0] - O[0])


# ---------------------------------------------------------------------------
# 2. Euclidean distance
# ---------------------------------------------------------------------------
def dist(P: Point, Q: Point) -> float:
    """
    Euclidean distance between P and Q.

    Formula:
        dist(P, Q) = sqrt((Q.x - P.x)^2 + (Q.y - P.y)^2)

    Uses math.hypot for numerical stability.
    """
    return math.hypot(Q[0] - P[0], Q[1] - P[1])


# ---------------------------------------------------------------------------
# 3. Convex Hull — Andrew's Monotone Chain
# ---------------------------------------------------------------------------
def convex_hull(points: List[Point]) -> List[Point]:
    """
    Computes the convex hull of a 2-D point set using Andrew's Monotone Chain.

    Steps:
        1. Sort points lexicographically by (x, y).
        2. Build lower hull (left → right): discard points causing a
           clockwise turn or collinearity (cross <= 0).
        3. Build upper hull (right → left): same rule.
        4. Concatenate lower and upper hulls, removing shared endpoints.

    Time complexity: O(M log M) where M = len(points)
    Space complexity: O(M)

    Returns:
        Convex hull vertices in counter-clockwise order.
        Collinear points on hull edges are excluded (strict convex hull).
    """
    points = sorted(set(points))  # deduplicate, then sort by (x, y)
    n = len(points)

    if n <= 1:
        return points

    # Build lower hull (left to right)
    lower: List[Point] = []
    for p in points:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)

    # Build upper hull (right to left)
    upper: List[Point] = []
    for p in reversed(points):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)

    # Remove duplicated endpoints shared between lower and upper hulls
    return lower[:-1] + upper[:-1]


# ---------------------------------------------------------------------------
# 4. Hull perimeter
# ---------------------------------------------------------------------------
def hull_perimeter(hull: List[Point]) -> float:
    """
    Computes the perimeter of a convex polygon defined by hull vertices.

    Formula:
        perimeter = sum of dist(H[i], H[(i+1) mod k])  for i = 0..k-1

    Degenerate cases:
        0 or 1 point → 0.0  (single machine at a point)
        2 points     → 2 * dist  (collinear: travel back and forth)
    """
    k = len(hull)
    if k <= 1:
        return 0.0
    if k == 2:
        return 2.0 * dist(hull[0], hull[1])

    total = 0.0
    for i in range(k):
        total += dist(hull[i], hull[(i + 1) % k])
    return total


# ---------------------------------------------------------------------------
# 5. Main
# ---------------------------------------------------------------------------
def main():
    """
    Reads N rectangles from stdin.
    Each rectangle: x1 y1 x2 y2  (two opposite corners, axis-aligned).
    Outputs the minimum patrol path length with precision >= 10^-6.
    """
    data = sys.stdin.read().split()
    idx = 0

    n = int(data[idx]); idx += 1

    points: List[Point] = []
    for _ in range(n):
        x1 = float(data[idx]); idx += 1
        y1 = float(data[idx]); idx += 1
        x2 = float(data[idx]); idx += 1
        y2 = float(data[idx]); idx += 1
        # All four corners of the rectangle
        points.append((x1, y1))
        points.append((x2, y1))
        points.append((x1, y2))
        points.append((x2, y2))

    hull  = convex_hull(points)
    perim = hull_perimeter(hull)

    # Print with 9 decimal places — satisfies the 10^-6 error requirement
    print(f"{perim:.9f}")


if __name__ == "__main__":
    main()
