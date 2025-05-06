#include <mpi.h>
#include <omp.h>
#include <vector>
#include <algorithm>
#include <iostream>
#include <numeric>
#include <cstdint>
#include <chrono>

// Type alias for a permutation
using perm_t = std::vector<int64_t>;

// Precompute factorials up to 20!
static int64_t fact[21] = {1};
void init_factorials(){
    for(int i = 1; i <= 20; ++i)
        fact[i] = fact[i-1] * i;
}

// Unrank: convert a factoradic index in [0, n!-1] to the permutation
perm_t unrank(int64_t idx, int n){
    perm_t elements(n);
    std::iota(elements.begin(), elements.end(), 1);
    perm_t result(n);
    int64_t remain = idx;
    for(int pos = 0; pos < n; ++pos){
        int64_t f = fact[n-1-pos];
        int64_t sel = remain / f;
        result[pos] = elements[sel];
        elements.erase(elements.begin() + sel);
        remain %= f;
    }
    return result;
}

// Identity permutation (1,2,…,n)
perm_t identity(int n){
    perm_t v(n);
    std::iota(v.begin(), v.end(), 1);
    return v;
}

// Rightmost index where v[i] != i+1
int r_index(const perm_t &v){
    for(int i=(int)v.size()-1; i>=0; --i)
        if(v[i] != i+1) return i;
    return -1;
}

// Swap element x with its right neighbor
perm_t swap_elem(const perm_t &v, int64_t x){
    perm_t w = v;
    auto it = std::find(w.begin(), w.end(), x);
    int i = std::distance(w.begin(), it);
    std::swap(w[i], w[i+1]);
    return w;
}

// “FindPosition” from Algorithm 1
perm_t find_position(const perm_t &v, int t, int n){
    perm_t root = identity(n);
    // Rule (1.1)
    if(t==2 && swap_elem(v,t)==root)
        return swap_elem(v,t-1);
    // Rule (1.2)
    if(v[n-2]==t || v[n-2]==n-1){
        int j = r_index(v);
        return swap_elem(v, v[j]);
    }
    // Rule (1.3)
    return swap_elem(v, t);
}

// “Parent1” from Algorithm 1
perm_t parent1(const perm_t &v, int t, int n){
    perm_t root = identity(n);
    // Case A: last symbol = n
    if(v.back()==n){
        if(t!=n-1) return find_position(v,t,n);
        return swap_elem(v, v[n-2]);
    }
    // Case B.2: (n-1,n) at end
    if(v.back()==n-1 && v[n-2]==n && swap_elem(v,n)!=root){
        return (t==1 ? swap_elem(v,n) : swap_elem(v,t-1));
    }
    // Case C
    if(v.back()==t) return swap_elem(v,n);
    return swap_elem(v,t);
}

int main(int argc, char** argv){
    MPI_Init(&argc, &argv);
    int rank, size;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    init_factorials();

    // parse n (up to 12)
    int n = 4;
    if(argc > 1) n = std::atoi(argv[1]);
    if(n < 3 || n > 12){
        if(rank==0) std::cerr<<"Error: choose 3 ≤ n ≤ 12\n";
        MPI_Abort(MPI_COMM_WORLD, 1);
    }

    // total permutations = n!
    int64_t total = fact[n];
    perm_t root = identity(n);

    // block‐distribute index range [0 .. total-1]
    int64_t base = total / size;
    int64_t rem  = total % size;
    int64_t start, end;
    if(rank < rem){
        start = rank * (base+1);
        end   = start + (base+1);
    } else {
        start = rem * (base+1) + (rank-rem)*base;
        end   = start + base;
    }

    // local counts for trees t=1..n-1
    std::vector<int64_t> local_counts(n-1, 0);

    // Start measuring execution time
    double start_time = MPI_Wtime();

    // Parallel loop over our index slice
    #pragma omp parallel
    {
        std::vector<int64_t> priv(n-1, 0);
        #pragma omp for schedule(dynamic)
        for(int64_t idx = start; idx < end; ++idx){
            perm_t v = unrank(idx, n);
            if(v == root) continue;
            for(int t=1; t<n; ++t){
                (void)parent1(v, t, n);
                priv[t-1]++;
            }
        }
        #pragma omp critical
        for(int i=0; i<n-1; ++i) local_counts[i] += priv[i];
    }

    // Reduce to global counts
    std::vector<int64_t> global_counts(n-1, 0);
    MPI_Reduce(
      local_counts.data(), global_counts.data(),
      n-1, MPI_LONG_LONG, MPI_SUM, 0, MPI_COMM_WORLD
    );

    // Stop measuring execution time
    double end_time = MPI_Wtime();
    double exec_time = end_time - start_time;

    // Rank 0 prints verification and execution time
    if(rank==0){
        std::cout << "Total execution time for n = " << n 
                  << " with " << omp_get_max_threads() << " threads: "
                  << exec_time << " seconds.\n";

        // Your existing summary printout or other information
    }

    MPI_Finalize();
    return 0;
}
