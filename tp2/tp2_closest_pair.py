#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TP2 - Closest Pair of Points in R^2 (Divide & Conquer) - O(n log n)

Implements the classic closest-pair algorithm:
- Pre-sort points by x and y.
- Recurse on halves.
- Merge step checks only a bounded number of neighbors in the strip.

Usage:
  python tp2_closest_pair.py --examples
  python tp2_closest_pair.py --random 10 --seed 42
  python tp2_closest_pair.py --points "0,0" "1,2" "3,4"
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import List, Tuple, Optional
import argparse
import math
import random


@dataclass(frozen=True)
class Point:
    x: float
    y: float

    @staticmethod
    def from_str(s: str) -> "Point":
        parts = s.split(",")
        if len(parts) != 2:
            raise ValueError(f"Point must be 'x,y'. Got: {s!r}")
        return Point(float(parts[0]), float(parts[1]))


def dist(p: Point, q: Point) -> float:
    dx = p.x - q.x
    dy = p.y - q.y
    return math.hypot(dx, dy)


def brute_force(points: List[Point]) -> Tuple[float, Tuple[Point, Point]]:
    best = float("inf")
    pair = (points[0], points[0])
    n = len(points)
    for i in range(n):
        for j in range(i + 1, n):
            d = dist(points[i], points[j])
            if d < best:
                best = d
                pair = (points[i], points[j])
    return best, pair


def closest_pair(points: List[Point]) -> Tuple[float, Tuple[Point, Point]]:
    """
    Returns: (min_distance, (p*, q*))
    Complexity: O(n log n) time, O(n) extra memory (for y-sorted lists).
    """
    if len(points) < 2:
        raise ValueError("Need at least two points.")

    px = sorted(points, key=lambda p: (p.x, p.y))
    py = sorted(points, key=lambda p: (p.y, p.x))

    d, pair = _closest_pair_rec(px, py)
    return d, pair


def _closest_pair_rec(px: List[Point], py: List[Point]) -> Tuple[float, Tuple[Point, Point]]:
    n = len(px)
    if n <= 3:
        return brute_force(px)

    mid = n // 2
    Qx = px[:mid]
    Rx = px[mid:]
    midx = Qx[-1].x

    Qset = set(Qx)
    Qy = [p for p in py if p in Qset]
    Ry = [p for p in py if p not in Qset]

    dl, pair_l = _closest_pair_rec(Qx, Qy)
    dr, pair_r = _closest_pair_rec(Rx, Ry)

    if dl <= dr:
        d = dl
        best_pair = pair_l
    else:
        d = dr
        best_pair = pair_r

    # Build strip within d of mid line, sorted by y already (because taken from py)
    strip = [p for p in py if abs(p.x - midx) < d]

    # Check only next up to 7 points for each point in strip
    m = len(strip)
    for i in range(m):
        for j in range(i + 1, min(i + 8, m)):
            dd = dist(strip[i], strip[j])
            if dd < d:
                d = dd
                best_pair = (strip[i], strip[j])

    return d, best_pair


def example_sets() -> List[List[Point]]:
    return [
        [Point(0, 0), Point(2, 3), Point(3, 4), Point(5, 1), Point(1, 1),
         Point(4, 4), Point(7, 2), Point(6, 6), Point(8, 5), Point(9, 1)],
        [Point(-5, -4), Point(-3, 2), Point(0, 0), Point(1, 1), Point(2, 2),
         Point(10, 10), Point(10, 11), Point(11, 10), Point(3, -1), Point(4, -2)],
        [Point(0.1, 0.1), Point(0.2, 0.2), Point(0.3, 0.3), Point(5, 5), Point(6, 6),
         Point(7, 7), Point(8, 8), Point(9, 9), Point(1.0, 1.01), Point(1.02, 1.03)],
    ]


def random_points(n: int, seed: int) -> List[Point]:
    rng = random.Random(seed)
    pts = []
    for _ in range(n):
        pts.append(Point(rng.randint(-50, 50), rng.randint(-50, 50)))
    return pts


def fmt_point(p: Point) -> str:
    # avoid trailing .0 noise when integer-like
    def f(v: float) -> str:
        if abs(v - round(v)) < 1e-9:
            return str(int(round(v)))
        return f"{v:.5g}"
    return f"({f(p.x)}, {f(p.y)})"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--examples", action="store_true", help="Run the 3 required example sets (n=10 each).")
    ap.add_argument("--random", type=int, help="Generate N random points and run.")
    ap.add_argument("--seed", type=int, default=42, help="Seed for --random. Default: 42")
    ap.add_argument("--points", nargs="*", help="Explicit points as 'x,y'. Example: --points 0,0 1,2 2,2")
    args = ap.parse_args()

    batches: List[Tuple[str, List[Point]]] = []

    if args.examples:
        for k, pts in enumerate(example_sets(), start=1):
            batches.append((f"Example {k}", pts))

    if args.random is not None:
        batches.append((f"Random n={args.random} seed={args.seed}", random_points(args.random, args.seed)))

    if args.points:
        pts = [Point.from_str(s) for s in args.points]
        batches.append(("Manual", pts))

    if not batches:
        ap.error("Choose: --examples, --random N, o --points ...")

    for name, pts in batches:
        d, (p, q) = closest_pair(pts)
        print(f"\n=== {name} ===")
        print("Points:", ", ".join(fmt_point(p) for p in pts))
        print(f"Closest pair: {fmt_point(p)} and {fmt_point(q)}")
        print(f"Minimum distance: {d:.6f}")

if __name__ == "__main__":
    main()
