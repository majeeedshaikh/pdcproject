#!/usr/bin/env bash
# scripts/benchmark.sh — strong‐scaling benchmark with averaging

# Go to project root
cd "$(dirname "$0")/.."

N=6
BIN=bin/parallel
REPEATS=20

mkdir -p results
echo "P,T,avg_time_s" > results/results.csv

for P in 1 2 4; do
  for T in 1 2 4; do
    export OMP_NUM_THREADS=$T

    # accumulate time in nanoseconds
    total_ns=0
    for i in $(seq 1 $REPEATS); do
      start_ns=$(date +%s%N)
      mpirun -n $P $BIN $N > /dev/null
      end_ns=$(date +%s%N)
      run_ns=$((end_ns - start_ns))
      total_ns=$((total_ns + run_ns))
    done

    # compute average in seconds (with 3 decimal places)
    avg_s=$(awk "BEGIN { printf \"%.3f\", $total_ns/($REPEATS*1e9) }")
    echo "$P,$T,$avg_s" >> results/results.csv
    echo "Done P=$P, T=$T → avg $avg_s s over $REPEATS runs"
  done
done
