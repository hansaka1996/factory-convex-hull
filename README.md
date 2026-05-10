# Optimal Patrol Path Around Machines

**Programming Assessment — Computational Geometry**

## Problem

A factory floor contains **N axis-aligned rectangular machines**. A security robot must patrol around all of them along the **shortest possible simple closed loop** that:
- Does not pass through the interior of any rectangle
- Encloses all rectangles entirely

## Approach

The optimal path is the **perimeter of the convex hull** of all rectangle corner points.

### Why?

1. **Rectangles → Points:** Every rectangle contributes 4 corner points. The enclosing loop only ever needs to bend at corners, so we reduce N rectangles to at most 4N points.
2. **Convexity is optimal:** Any non-convex enclosing path can be shortened by cutting off concavities (replacing a dent with a straight chord). The shortest enclosing polygon is therefore convex.
3. **Convex hull is tightest:** The convex hull is the smallest convex set containing all points. Any other convex enclosing polygon has a perimeter at least as large.

### Algorithm — Andrew's Monotone Chain

| Step | Operation | Complexity |
|------|-----------|------------|
| Extract corners | 4 corners per rectangle | O(N) |
| Sort points | Lexicographic (x, y) | **O(N log N)** |
| Build lower hull | Left → right, discard CW turns | O(N) |
| Build upper hull | Right → left, discard CW turns | O(N) |
| Compute perimeter | Sum of edge lengths | O(k) ⊆ O(N) |
| **Total** | | **O(N log N)** |

## Mathematical Details

**Orientation test (cross product):**
```
cross(O, A, B) = (A.x − O.x)(B.y − O.y) − (A.y − O.y)(B.x − O.x)
  > 0  →  counter-clockwise (left turn)
  = 0  →  collinear
  < 0  →  clockwise (right turn)
```

**Euclidean distance:**
```
dist(P, Q) = sqrt((Q.x − P.x)² + (Q.y − P.y)²)
```

**Hull perimeter:**
```
perimeter = Σ dist(H[i], H[(i+1) mod k])   for i = 0 .. k−1
```

## Project Structure

```
├── solution.py     # Main solution — O(N log N)
├── tests.py        # Sample test cases with expected outputs
└── README.md
```

## Usage

**Run from stdin:**
```bash
python solution.py < input.txt
```

**Input format:**
```
N
x1 y1 x2 y2
x1 y1 x2 y2
...
```
- First line: integer N (number of rectangles), 1 ≤ N ≤ 2×10⁵
- Each subsequent line: two opposite corners of a rectangle
- Coordinates: real numbers with |value| ≤ 10⁶

**Output:** A single real number — the minimum path length, with absolute/relative error ≤ 10⁻⁶.

## Sample Test Cases

### Test 1 — Single unit square
```
Input:          Output:
1               4.000000000
0 0 1 1
```

### Test 2 — Two separated rectangles
```
Input:          Output:
2               10.000000000
0 0 1 1
3 0 4 1
```
Hull: (0,0) → (4,0) → (4,1) → (0,1) — a 4×1 bounding rectangle.

### Test 3 — Nested rectangles
```
Input:          Output:
2               12.000000000
0 0 3 3
1 1 2 2
```
Inner rectangle is fully inside outer; hull is just the outer rectangle. Perimeter = 2×(3+3) = 12.

### Test 4 — Floating-point coordinates
```
Input:          Output:
1               6.000000000
0.5 0.5 2.0 2.5
```
Width = 1.5, Height = 2.0. Perimeter = 2×(1.5+2.0) = 7.000000000.

## Requirements

- Python 3.7+
- No external libraries — uses only `sys`, `math`, and `typing` from the standard library

## Function Overview

| Function | Purpose |
|----------|---------|
| `cross(O, A, B)` | Signed cross product — orientation test |
| `dist(P, Q)` | Euclidean distance between two points |
| `convex_hull(points)` | Andrew's Monotone Chain — returns hull vertices CCW |
| `hull_perimeter(hull)` | Sum of edge lengths around the hull |
| `main()` | Reads input, runs pipeline, prints result |
