#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TP3 - Needleman–Wunsch (Global Alignment) - O(nm)

Scoring:
  match = +1
  mismatch = -1
  gap = -2

Outputs:
- full score matrix
- one optimal global alignment
- final score

Usage:
  python tp3_needleman_wunsch.py --examples
  python tp3_needleman_wunsch.py --seq1 GATTACA --seq2 GCATGCU
"""

from __future__ import annotations
import argparse
from dataclasses import dataclass
from typing import List, Tuple


@dataclass(frozen=True)
class NWConfig:
    match: int = 1
    mismatch: int = -1
    gap: int = -2


def score(a: str, b: str, cfg: NWConfig) -> int:
    return cfg.match if a == b else cfg.mismatch


def needleman_wunsch(s1: str, s2: str, cfg: NWConfig) -> Tuple[List[List[int]], str, str, int]:
    """
    Returns: (matrix, aligned_s1, aligned_s2, final_score)
    """
    n = len(s1)
    m = len(s2)

    # DP matrix (n+1) x (m+1)
    F = [[0] * (m + 1) for _ in range(n + 1)]

    # init
    for i in range(1, n + 1):
        F[i][0] = F[i - 1][0] + cfg.gap
    for j in range(1, m + 1):
        F[0][j] = F[0][j - 1] + cfg.gap

    # fill matrix
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            diag = F[i - 1][j - 1] + score(s1[i - 1], s2[j - 1], cfg)
            up = F[i - 1][j] + cfg.gap      # gap in s2
            left = F[i][j - 1] + cfg.gap    # gap in s1
            F[i][j] = max(diag, up, left)

    # traceback (prefer diag, then up, then left for determinism)
    i, j = n, m
    a1: List[str] = []
    a2: List[str] = []
    while i > 0 or j > 0:
        if i > 0 and j > 0:
            diag_score = F[i - 1][j - 1] + score(s1[i - 1], s2[j - 1], cfg)
        else:
            diag_score = None

        up_score = F[i - 1][j] + cfg.gap if i > 0 else None
        left_score = F[i][j - 1] + cfg.gap if j > 0 else None

        cur = F[i][j]

        if diag_score is not None and cur == diag_score:
            a1.append(s1[i - 1])
            a2.append(s2[j - 1])
            i -= 1
            j -= 1
        elif up_score is not None and cur == up_score:
            a1.append(s1[i - 1])
            a2.append("-")
            i -= 1
        else:
            a1.append("-")
            a2.append(s2[j - 1])
            j -= 1

    a1.reverse()
    a2.reverse()

    return F, "".join(a1), "".join(a2), F[n][m]


def format_matrix(F: List[List[int]], s1: str, s2: str) -> str:
    # Pretty print with labels
    # Top header: _ plus s2 chars
    col_labels = ["_"] + list(s2)
    row_labels = ["_"] + list(s1)

    # Determine width
    w = max(len(str(x)) for row in F for x in row)
    w = max(w, 2)

    lines = []
    header = " " * (w + 1) + " ".join(f"{c:>{w}}" for c in col_labels)
    lines.append(header)
    for i, row in enumerate(F):
        label = row_labels[i]
        lines.append(f"{label:>{w}} " + " ".join(f"{v:>{w}}" for v in row))
    return "\n".join(lines)


def run_pair(s1: str, s2: str, cfg: NWConfig) -> None:
    F, a1, a2, sc = needleman_wunsch(s1, s2, cfg)
    print("\n============================================================")
    print(f"Sequence 1: {s1}")
    print(f"Sequence 2: {s2}")
    print("\Score matrix:")
    print(format_matrix(F, s1, s2))
    print("\nOptimal alignment (global):")
    print(a1)
    print(a2)
    print(f"\Total score: {sc}")
    print("============================================================")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--seq1", type=str, help="Sequence 1 (ej: GATTACA)")
    ap.add_argument("--seq2", type=str, help="Sequence 2 (ej: GCATGCU)")
    ap.add_argument("--examples", action="store_true", help="Run the 3 examples from the statement.")
    args = ap.parse_args()

    cfg = NWConfig(match=1, mismatch=-1, gap=-2)

    if args.examples:
        pairs = [
            ("GATTACA", "GCATGCU"),
            ("ACGT", "ACCT"),
            ("ATGCT", "AGCT"),
        ]
        for s1, s2 in pairs:
            run_pair(s1, s2, cfg)
        return

    if args.seq1 and args.seq2:
        run_pair(args.seq1.strip().upper(), args.seq2.strip().upper(), cfg)
        return

    ap.error("Use --examples or pass --seq1 and --seq2.")


if __name__ == "__main__":
    main()
