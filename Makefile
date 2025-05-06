# Detect Homebrew prefixes
BREW_PREFIX      := $(shell brew --prefix)
OPENMPI_PREFIX  := $(BREW_PREFIX)/opt/open-mpi
LIBOMP_PREFIX   := $(BREW_PREFIX)/opt/libomp

# Compilers (override on command line if needed)
#CXX   ?= /opt/homebrew/opt/llvm/bin/clang++     # for prod build
CXX   ?= /opt/homebrew/opt/llvm/bin/clang++


GXX   ?= /opt/homebrew/opt/llvm/bin/g++         # for gprof build (install via `brew install gcc`)

SRC              := src/parallel.cpp
PROD_BIN         := bin/parallel
GPROF_BIN        := bin/parallel_gprof

# Common flags
CXXFLAGS        := -std=c++17 -O3 -fopenmp -Xpreprocessor -fopenmp
LDFLAGS         := \
    -I$(LIBOMP_PREFIX)/include -L$(LIBOMP_PREFIX)/lib -lomp \
    -I$(OPENMPI_PREFIX)/include -L$(OPENMPI_PREFIX)/lib -lmpi


.PHONY: all prod gprof clean

all: prod gprof

prod: $(PROD_BIN)

$(PROD_BIN): $(SRC)
	@mkdir -p $(dir $@)
	@echo "[prod] Building $@ with Clang+MPI+OpenMP"
	OMPI_CXX=$(CXX) mpicxx $(CXXFLAGS) $(LDFLAGS) -o $@ $<

gprof: $(GPROF_BIN)

$(GPROF_BIN): $(SRC)
	@mkdir -p $(dir $@)
	@echo "[gprof] Building $@ with GNU g++-MPI+OpenMP+gprof"
	OMPI_CXX=$(GXX) mpicxx $(CXXFLAGS) $(LDFLAGS) -pg -o $@ $<

clean:
	@echo "[clean] Removing binaries and profiles"
	rm -f $(PROD_BIN) $(GPROF_BIN)
	rm -rf profiles/gmon.out.* profiles/gprof_rank*.txt
