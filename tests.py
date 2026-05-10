"""
tests.py — Sample test cases for the Optimal Patrol Path solution.

Run:
    python tests.py
"""

import math
import io
import sys
from solution import convex_hull, hull_perimeter, cross, dist


def run_solution(input_str: str) -> float:
    """Helper: run the full pipeline on a raw input string."""
    data = input_str.split()
    idx = 0
    n = int(data[idx]); idx += 1
    points = []
    for _ in range(n):
        x1 = float(data[idx]); idx += 1
        y1 = float(data[idx]); idx += 1
        x2 = float(data[idx]); idx += 1
        y2 = float(data[idx]); idx += 1
        points += [(x1,y1),(x2,y1),(x1,y2),(x2,y2)]
    hull = convex_hull(points)
    return hull_perimeter(hull)


def approx_equal(a: float, b: float, tol: float = 1e-6) -> bool:
    return abs(a - b) <= tol * max(1.0, abs(b))


TESTS = [
    # (name, input_str, expected_perimeter)
    (
        "Single unit square",
        "1\n0 0 1 1",
        4.0,
    ),
    (
        "Two horizontally separated rectangles",
        "2\n0 0 1 1\n3 0 4 1",
        10.0,
    ),
    (
        "Nested rectangles (inner inside outer)",
        "2\n0 0 3 3\n1 1 2 2",
        12.0,
    ),
    (
        "Single rectangle — float coords",
        "1\n0.5 0.5 2.0 2.5",
        7.0,           # 2*(1.5+2.0)
    ),
    (
        "Two touching rectangles (share an edge)",
        "2\n0 0 1 1\n1 0 2 1",
        6.0,           # hull is 2×1 rectangle, perimeter=6
    ),
    (
        "Three rectangles in an L-shape",
        "3\n0 0 2 1\n0 0 1 2\n2 1 3 2",
        # Hull: (0,0)→(2,0)→(3,1)→(3,2)→(0,2)
        # Perimeter: 2 + sqrt(2) + 1 + 3 + 2 = 9.41421356...
        2 + math.sqrt(2) + 1 + 3 + 2,
    ),
    (
        "All identical rectangles",
        "3\n0 0 1 1\n0 0 1 1\n0 0 1 1",
        4.0,           # deduplication → same as single square
    ),
    (
        "Single point rectangle (degenerate)",
        "1\n2 3 2 3",
        0.0,
    ),
    (
        "Collinear rectangles on x-axis",
        "3\n0 0 1 0\n2 0 3 0\n4 0 5 0",
        # All points on y=0; hull is segment [0,0]→[5,0]; perimeter=2*5=10
        10.0,
    ),
]


def main():
    passed = 0
    failed = 0
    for name, inp, expected in TESTS:
        result = run_solution(inp)
        ok = approx_equal(result, expected)
        status = "PASS" if ok else "FAIL"
        if ok:
            passed += 1
        else:
            failed += 1
        print(f"[{status}] {name}")
        if not ok:
            print(f"       Expected: {expected:.9f}")
            print(f"       Got:      {result:.9f}")

    print(f"\n{'='*45}")
    print(f"Results: {passed}/{passed+failed} tests passed")
    if failed == 0:
        print("All tests passed ✓")
    else:
        print(f"{failed} test(s) failed")


if __name__ == "__main__":
    main()
