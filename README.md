# Parallel and Distributed Computing Project

Overview
This repository contains the materials for Phase 1 of the Parallel and Distributed Computing (PDC) project, due April 20, 2025. The project focuses on analyzing the research paper "A parallel algorithm for constructing multiple independent spanning trees in bubble-sort networks" by Shih-Shun Kao, Ralf Klasing, Ling-Ju Hung, Chia-Wei Lee, and Sun-Yuan Hsieh (2023). Phase 1 involves studying the paper, preparing a presentation, and proposing a parallelization strategy using METIS, MPI, and OpenMP/OpenCL.
Project Objectives

Paper Analysis: Understand the problem, proposed parallel algorithm, results, and contributions of the paper.
Presentation: Develop a 10-15 minute presentation summarizing the paper and proposing a parallelization strategy, to be delivered starting April 21, 2025.
Parallelization Strategy: Design an implementation approach using METIS for graph partitioning, MPI for inter-node communication, and OpenMP/OpenCL for intra-node parallelism.

Paper Summary
Problem Addressed
The paper tackles the construction of multiple independent spanning trees (ISTs) in bubble-sort networks (( B_n )), which are Cayley graphs with vertices as permutations of ( {1, 2, ..., n} ). ISTs are critical for fault-tolerant broadcasting and secure message distribution, but a previous recursive algorithm (Kao et al., 2019) was hard to parallelize, leaving an open problem.
Proposed Parallel Algorithm
The paper introduces a non-recursive, fully parallelized algorithm (Algorithm 1) that constructs ( n-1 ) ISTs rooted at the identity permutation. Each vertex computes its parent in constant time using auxiliary functions (FindPosition, Swap) and a pre-processing step, enabling efficient parallel computation.
Results Obtained

Time Complexity: ( O(n . n!) ), asymptotically optimal for ( n! ) vertices and ( n-1 ) trees.
Correctness: Constructs ( n-1 ) ISTs with vertex-disjoint paths (Theorem 1).
Tree Height: At most ( n(n-1)/2 + n-1 ) (Theorem 2), ensuring efficient communication.

Key Contributions

Solves the open problem with a parallel, non-recursive algorithm.
Achieves optimal complexity and maximum ISTs (( n-1 )).
Enhances fault tolerance and security in interconnection networks.
Suggests future work on ((n, k))-bubble-sort and butterfly graphs.

Parallelization Strategy
To implement the algorithm:

METIS: Partition the ( B_n ) graph into balanced subgraphs to minimize edge cuts.
MPI: Distribute subgraphs to processes and manage inter-node communication, which is minimal due to independent computations.
OpenMP/OpenCL: Parallelize parent computations within each subgraph, leveraging multi-core CPUs (OpenMP) or GPUs (OpenCL).
Workflow: Partition graph, distribute via MPI, compute in parallel, and combine results.

Repository Contents

Presentation slides (10 slides) covering the paper and parallelization strategy, including visuals (Figures 1-7 from the paper).
Supporting materials, such as the paper PDF and project requirements (PDC Project.pdf).

Next Steps

Phase 1: Finalize and submit presentation slides by April 20, 2025, and deliver the presentation starting April 21, 2025.
Phase 2: Implement the algorithm using the proposed parallelization strategy and evaluate its scalability.

References

Kao, S.-S., Klasing, R., Hung, L.-J., Lee, C.-W., & Hsieh, S.-Y. (2023). A parallel algorithm for constructing multiple independent spanning trees in bubble-sort networks. Journal of Parallel and Distributed Computing. [DOI: 10.1016/j.jpdc.2023.104749]

Contributors

Affan Ali

Abdul Majeed

Abdul Wasay

Feel free to contact us for questions or feedback!
