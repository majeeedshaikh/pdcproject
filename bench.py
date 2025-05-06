#!/usr/bin/env python3
"""
bench.py — strong-scaling benchmark using Python for nanosecond timing
"""

import subprocess, time, csv, os

# Parameters
N = 6
BIN = "bin/parallel"
REPEATS = 20
RESULTS = "results/results.csv"

# Ensure results dir exists
os.makedirs("results", exist_ok=True)

with open(RESULTS, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["P","T","avg_time_s"])
    for P in [1,2,4]:
        for T in [1,2,4]:
            os.environ["OMP_NUM_THREADS"] = str(T)
            total_ns = 0
            for _ in range(REPEATS):
                t0 = time.time_ns()
                subprocess.run(["mpirun","-n",str(P),BIN,str(N)],
                               stdout=subprocess.DEVNULL, check=True)
                t1 = time.time_ns()
                total_ns += (t1 - t0)
            avg_s = total_ns / (REPEATS * 1e9)
            writer.writerow([P, T, f"{avg_s:.3f}"])
            print(f"Done P={P}, T={T} → avg {avg_s:.3f}s over {REPEATS}")
