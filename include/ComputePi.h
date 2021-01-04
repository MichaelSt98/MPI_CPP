//
// Created by Michael Staneker on 04.01.21.
//

#ifndef MPI_CPP_COMPUTEPI_H
#define MPI_CPP_COMPUTEPI_H

#include <mpi.h>
#include <iostream>
#include <iomanip>
#include <cmath>
#include <cstdlib>


class ComputePi {
public:
    int nproc;
    int rank;
    long N;
    long sum;
    ComputePi(long Iterations);

    double drand();
    void set_seed(int p);
    long monte_carlo();
    void calculate_pi();
};


#endif //MPI_CPP_COMPUTEPI_H
