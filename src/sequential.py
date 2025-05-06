#!/usr/bin/env python3
"""
sequential.py

Compute the n-1 independent spanning trees on the bubble-sort network B_n
by implementing Algorithm 1 (Parent1) from the paper.
"""

import argparse
import itertools
from math import factorial

def identity(n):
    return tuple(range(1, n+1))

def r_index(v):
    for i in range(len(v)-1, -1, -1):
        if v[i] != i+1:
            return i
    raise ValueError("r_index on identity")

def swap(v, x):
    v = list(v)
    i = v.index(x)
    if i == len(v)-1:
        raise ValueError(f"Cannot swap {x} in {v}")
    v[i], v[i+1] = v[i+1], v[i]
    return tuple(v)

def find_position(v, t, n):
    root = identity(n)
    # Rule (1.1)
    if t == 2 and swap(v, t) == root:
        return swap(v, t-1)
    # Rule (1.2)
    elif v[n-2] in (t, n-1):
        j = r_index(v)
        return swap(v, v[j])
    # Rule (1.3)
    else:
        return swap(v, t)

def parent1(v, t, n):
    root = identity(n)
    # Case A
    if v[-1] == n:
        if t != n-1:
            return find_position(v, t, n)
        else:
            return swap(v, v[-2])
    # Case B & C
    if v[-1] == n-1 and v[-2] == n and swap(v, n) != root:
        return swap(v, n) if t == 1 else swap(v, t-1)
    if v[-1] == t:
        return swap(v, n)
    return swap(v, t)

def build_and_verify(n):
    perms = list(itertools.permutations(range(1, n+1)))
    root = identity(n)
    total = factorial(n)
    summary = []
    for t in range(1, n):
        edges = [(v, parent1(v, t, n)) for v in perms if v != root]
        ok = len(edges) == total-1 and len(set(edges)) == total-1
        summary.append((t, len(edges), ok))
    return summary

def example_runs(n):
    tests = [((4,2,3,1),1), ((5,4,3,2,1),2), ((3,1,2),1)]
    print("Example Parent1 outputs:")
    for v, t in tests:
        if len(v)==n and 1<=t<n:
            print(f" v={v}, t={t} → {parent1(v,t,n)}")

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--n", type=int, default=4, help="3 ≤ n ≤ 6")
    args = p.parse_args()
    n = args.n
    if not (3 <= n <= 6):
        raise SystemExit("Choose n between 3 and 6")
    print(f"\nVerifying B_{n} sequential baseline…")
    for t, cnt, ok in build_and_verify(n):
        mark = "✓" if ok else "✗"
        print(f" Tree t={t}: {cnt}/{factorial(n)-1} edges {mark}")
    print()
    example_runs(n)
    print()
