#!/usr/bin/env python3
"""
mpi_impl.py

MPI-parallel IST parent-pointer computation using mpi4py + NumPy.
We scatter Σ_n evenly, compute each rank’s local edges per tree,
then Reduce with MPI.SUM to get correct global counts.
"""

import argparse
import itertools
from math import factorial
import numpy as np
from mpi4py import MPI

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
    if v[n-2] in (t, n-1):
        j = r_index(v)
        return swap(v, v[j])
    # Rule (1.3)
    return swap(v, t)

def parent1(v, t, n):
    root = identity(n)
    # Case A: last symbol = n
    if v[-1] == n:
        if t != n-1:
            return find_position(v, t, n)
        return swap(v, v[-2])
    # Case B.2: last two = (n-1,n)
    if v[-1] == n-1 and v[-2] == n and swap(v, n) != root:
        return swap(v, n) if t == 1 else swap(v, t-1)
    # Case C
    if v[-1] == t:
        return swap(v, n)
    return swap(v, t)

def main():
    # ---- parse arguments ----
    parser = argparse.ArgumentParser(
        description="MPI IST parent generator (3 ≤ n ≤ 6)"
    )
    parser.add_argument("--n", type=int, default=4, help="dimension n")
    args = parser.parse_args()
    n = args.n
    if not (3 <= n <= 6):
        raise SystemExit("Error: choose n between 3 and 6")

    # ---- MPI setup ----
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    # ---- build Σ_n on rank 0 ----
    if rank == 0:
        perms = list(itertools.permutations(range(1, n+1)))
        base, rem = divmod(len(perms), size)
        blocks = []
        idx = 0
        for i in range(size):
            length = base + (1 if i < rem else 0)
            blocks.append(perms[idx: idx+length])
            idx += length
    else:
        blocks = None

    # ---- scatter partitions ----
    local = comm.scatter(blocks, root=0)
    root_perm = identity(n)
    # remove the global root from your local list
    local = [v for v in local if v != root_perm]

    # ---- count local edges per tree into a NumPy array ----
    local_counts = np.zeros(n-1, dtype='i')
    for t_idx, t in enumerate(range(1, n)):
        for v in local:
            _ = parent1(v, t, n)  # compute parent
            local_counts[t_idx] += 1

    # ---- reduce into global_counts on rank 0 ----
    if rank == 0:
        global_counts = np.zeros_like(local_counts)
    else:
        global_counts = None

    comm.Reduce(
        [local_counts, MPI.INT],
        [global_counts, MPI.INT],
        op=MPI.SUM,
        root=0
    )

    # ---- rank 0 prints verification ----
    if rank == 0:
        total = factorial(n)
        print(f"\nMPI verification for B_{n} with {size} ranks:")
        for t_idx, cnt in enumerate(global_counts, start=1):
            ok = (cnt == total - 1)
            mark = "✓" if ok else "✗"
            print(f" Tree t={t_idx:>2}: total edges = {cnt}/{total-1} {mark}")
        print()

if __name__ == "__main__":
    main()
