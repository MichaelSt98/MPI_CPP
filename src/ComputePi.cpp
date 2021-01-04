//
// Created by Michael Staneker on 04.01.21.
//

#include "../include/ComputePi.h"

ComputePi::ComputePi(long Iterations) {
    MPI_Init(NULL, NULL);
    MPI_Comm_size(MPI_COMM_WORLD, &nproc);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    N = Iterations/nproc;
    sum = 0;
}

double ComputePi::drand() {
    const double fac = 1.0/(RAND_MAX-1.0);
    return fac*random();
}

void ComputePi::set_seed(int p) {
    srandom(p);
    for (int i=0; i<100; i++) drand();
}

long ComputePi::monte_carlo() {
    for (long i=0; i<N; i++) {
        double x = 2.0*(drand()-0.5); // Random value in [-1,1]
        double y = 2.0*(drand()-0.5); // Random value in [-1,1]
        double rsq = x*x + y*y;
        if (rsq < 1.0) sum++;
    }
    long total;
    MPI_Reduce(&sum, &total, 1, MPI_LONG, MPI_SUM, 0, MPI_COMM_WORLD);
    return total;
}

void ComputePi::calculate_pi() {

    set_seed(rank);
    long total = monte_carlo();

    if (rank == 0) {
        long double pi = (4.0L*total)/(N*nproc);
        std::cout << std::setprecision(8) << pi << std::endl;
    }

    //MPI_Finalize();
}
