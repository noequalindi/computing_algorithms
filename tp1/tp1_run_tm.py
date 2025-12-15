#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TP1 - Turing Machine: binary addition (multi-tape) in a YAML.

Runner of 2 tapes (infinite tape in both directions, integer indices).
Input: big-endian binary.

Example:
  python tp1_run_tm.py --a 1011 --b 111
"""

from __future__ import annotations
import argparse
from dataclasses import dataclass
from typing import Dict, Tuple
import yaml

BLANK = "_"

@dataclass(frozen=True)
class Transition:
    state: str
    write: Tuple[str, str]
    move: Tuple[str, str]  # 'L','R','N'


class SparseTape:
    def __init__(self, s: str):
        self.cells: Dict[int, str] = {}
        for i, ch in enumerate(s):
            self.cells[i] = ch

    def read(self, i: int) -> str:
        return self.cells.get(i, BLANK)

    def write(self, i: int, sym: str) -> None:
        if sym == BLANK:
            self.cells.pop(i, None)
        else:
            self.cells[i] = sym

    def to_string_trimmed(self) -> str:
        if not self.cells:
            return ""
        idxs = sorted(self.cells.keys())
        lo, hi = idxs[0], idxs[-1]
        return "".join(self.read(i) for i in range(lo, hi + 1)).strip(BLANK)

    def to_string_window(self, center: int, radius: int = 25) -> str:
        return "".join(self.read(i) for i in range(center - radius, center + radius + 1))


class MultiTapeTM:
    def __init__(self, spec: dict):
        self.spec = spec
        self.final_states = set(spec["final states"])
        self.state = spec["initial state"]

        trans = spec["transitions"]
        self.delta: Dict[Tuple[str, str, str], Transition] = {}
        for st, mapping in trans.items():
            for sym_key, t in mapping.items():
                s1, s2 = sym_key.split(",")
                w1, w2 = str(t["write"]).split(",")
                m1, m2 = str(t["move"]).split(",")
                self.delta[(st, s1, s2)] = Transition(
                    state=t["state"],
                    write=(w1, w2),
                    move=(m1, m2),
                )

        self.t1 = SparseTape("")
        self.t2 = SparseTape("")
        self.h1 = 0
        self.h2 = 0
        self.steps = 0

    def load(self, a: str, b: str) -> None:
        self.t1 = SparseTape(a)
        self.t2 = SparseTape(b)
        self.h1 = 0
        self.h2 = 0
        self.state = self.spec["initial state"]
        self.steps = 0

    def step(self) -> bool:
        if self.state in self.final_states:
            return False
        s1 = self.t1.read(self.h1)
        s2 = self.t2.read(self.h2)
        key = (self.state, s1, s2)
        if key not in self.delta:
            raise RuntimeError(f"Transition not defined for: {key}")
        tr = self.delta[key]
        self.t1.write(self.h1, tr.write[0])
        self.t2.write(self.h2, tr.write[1])
        self.h1 += (-1 if tr.move[0] == "L" else 1 if tr.move[0] == "R" else 0)
        self.h2 += (-1 if tr.move[1] == "L" else 1 if tr.move[1] == "R" else 0)
        self.state = tr.state
        self.steps += 1
        return True

    def run(self, max_steps: int = 200000) -> None:
        while self.steps < max_steps and self.step():
            pass
        if self.state not in self.final_states:
            raise RuntimeError(f"No halting in {max_steps} pasos. Estado actual: {self.state}")

    def result(self) -> str:
        s = self.t2.to_string_trimmed()
        if s == "":
            return "0"
        s = s.lstrip("0")
        return s if s else "0"


def validate_bin(s: str) -> str:
    s = s.strip()
    if s == "":
        return "0"
    if any(c not in "01" for c in s):
        raise ValueError("Just binary 0/1.")
    s = s.lstrip("0")
    return s if s else "0"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--a", required=True)
    ap.add_argument("--b", required=True)
    ap.add_argument("--yaml", default="binary_addition_patched.yaml")
    ap.add_argument("--max_steps", type=int, default=200000)
    ap.add_argument("--window", type=int, default=0, help="Si >0, imprime una ventana alrededor del head al final.")
    args = ap.parse_args()

    a = validate_bin(args.a)
    b = validate_bin(args.b)

    with open(args.yaml, "r", encoding="utf-8") as f:
        spec = yaml.safe_load(f)

    tm = MultiTapeTM(spec)
    tm.load(a, b)
    tm.run(max_steps=args.max_steps)

    print("============================================================")
    print(f"Entrada A (bin): {a}")
    print(f"Entrada B (bin): {b}")
    print(f"Resultado (bin): {tm.result()}")
    print(f"Pasos: {tm.steps}")
    print("Tape1 final (trim):", tm.t1.to_string_trimmed())
    print("Tape2 final (trim):", tm.t2.to_string_trimmed())
    if args.window > 0:
        print("Tape1 window:", tm.t1.to_string_window(tm.h1, args.window))
        print("Tape2 window:", tm.t2.to_string_window(tm.h2, args.window))
    print("============================================================")


if __name__ == "__main__":
    main()
