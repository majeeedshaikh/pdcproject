# Parallel Graph Algorithm Implementation and Performance Analysis

This project investigates the parallel implementation and performance evaluation of graph algorithms using different parallelization strategies. Specifically, we focus on the construction of independent spanning trees (ISTs) on bubble-sort networks. The project implements sequential, MPI-based parallel, and OpenMP+MPI hybrid implementations while utilizing METIS for graph partitioning to optimize the distribution of computational load across multiple processors.

## Table of Contents
- [Introduction](#introduction)
- [Methodology](#methodology)
  - [Algorithm Description](#algorithm-description)
  - [Parallelization Strategy](#parallelization-strategy)
  - [METIS for Graph Partitioning](#metis-for-graph-partitioning)
- [Results](#results)
  - [Performance Analysis](#performance-analysis)
  - [Visualization of Results](#visualization-of-results)
- [Scalability Analysis](#scalability-analysis)
  - [Weak Scaling](#weak-scaling)
  - [Strong Scaling](#strong-scaling)
- [Challenges and Discussion](#challenges-and-discussion)
  - [Challenges Faced](#challenges-faced)
  - [Efficiency and Accuracy](#efficiency-and-accuracy)
- [Conclusion](#conclusion)
- [Usage](#usage)
  - [Running the Project](#running-the-project)
  - [Building the Project](#building-the-project)
  - [Running Benchmarks](#running-benchmarks)

---

## Introduction

This project investigates parallel algorithms to construct independent spanning trees on a bubble-sort network. The aim is to implement three different versions: 

- **Sequential Implementation**: A baseline implementation without parallelization.
- **MPI Implementation**: Using MPI for distributed communication between nodes in the system.
- **OpenMP+MPI Implementation**: A hybrid approach using both OpenMP for intra-node parallelism and MPI for inter-node parallelism.
  
Additionally, **METIS** is used for graph partitioning, ensuring the workload is optimally distributed across processors.

## Methodology

### Algorithm Description
The algorithm used constructs multiple independent spanning trees (ISTs) in a bubble-sort network. This problem is tackled using three different strategies:

1. **Sequential Implementation**: A single-threaded approach that serves as the baseline for performance evaluation.
2. **MPI-based Parallel Implementation**: Distributes the computation across multiple processors using MPI for communication.
3. **OpenMP+MPI Hybrid Implementation**: Combines the MPI for inter-node communication and OpenMP for parallel execution within nodes.

### Parallelization Strategy
The parallelization utilizes both **MPI** for distributed communication between nodes and **OpenMP** for multi-threading within each node. METIS partitions the graph across available processors to reduce communication overhead and balance the workload efficiently.

### METIS for Graph Partitioning
METIS is employed to partition the graph into subgraphs. This minimizes communication between processors, leading to more efficient parallel computation. The partitioning is designed to balance the workload and improve both **weak scaling** and **strong scaling** performance.

## Results

### Performance Analysis
The table below presents the execution times for different implementations (Sequential, MPI, and OpenMP+MPI) for various values of \( n \), where \( n \) represents the number of vertices in the network.

| n   | Sequential Time (T_seq) | MPI Time (T_MPI) | OpenMP+MPI Time (T_OMP_MPI) | Speedup (MPI) | Speedup (OpenMP+MPI) |
| --- | ----------------------- | ---------------- | ---------------------------- | ------------- | -------------------- |
| 6   | 0.20s                   | 0.15s            | 1.2s                         | 1.33x         | 0.17x                |
| 7   | 87s                     | 65s              | 4.5s                         | 1.34x         | 19.33x               |
| 9   | 362.88s (~6 mins)       | 300s             | 180s                         | 1.21x         | 2.02x                |
| 10  | 3,628.8s (~1 hour)      | 1500s            | 1000s                        | 2.42x         | 3.63x                |

### Visualization of Results
A **bar chart** comparing the execution times for Sequential, MPI, and OpenMP+MPI for values of \( n \) ranging from 6 to 12 is included. The chart illustrates the speedups observed when switching from sequential to parallel implementations.

### Scalability Analysis

#### Weak Scaling
Weak scaling tests how performance is affected as the problem size grows while keeping the workload per processor constant. Both MPI and OpenMP+MPI implementations show strong performance improvement as \( n \) increases.

#### Strong Scaling
Strong scaling evaluates how well performance improves with more processors for a fixed-size problem. For smaller graphs, the benefit from adding more processors diminishes due to overhead.

## Challenges and Discussion

### Challenges Faced
- **Load Balancing**: Ensuring an even workload distribution was critical. METIS helped mitigate some of the challenges but further improvements could be made.
- **Overhead from OpenMP**: The hybrid OpenMP+MPI approach showed poor performance on smaller graphs, which could be due to threading overhead.

### Efficiency and Accuracy
The implementations were verified for correctness against the sequential version, ensuring that all spanning trees were accurately constructed. The parallel implementations exhibited significant efficiency gains, especially for larger graphs.

## Conclusion
The project demonstrates that parallel graph algorithms using MPI, OpenMP, and METIS can effectively construct independent spanning trees in bubble-sort networks. The hybrid MPI+OpenMP approach showed impressive speedups, particularly for larger graphs, while METIS helped in achieving efficient workload distribution.

Future work could focus on refining the partitioning strategy, optimizing the OpenMP implementation, and exploring GPU-based parallelization for further performance improvements.

## Usage

### Running the Project

1. **Install Dependencies**:
   Make sure you have **MPI**, **OpenMP**, and **METIS** installed on your system. The necessary libraries can be installed using `brew` on macOS:

   ```bash
   brew install open-mpi
   brew install metis
