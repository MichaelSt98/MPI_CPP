#include <iostream>
#include "../include/Simple_C_API.h"
#include "../include/Simple_boost_mpi.h"
#include "../include/ComputePi.h"

int main(int argc, char** argv) {

    std::cout << "Exploring MPI ..." << std::endl;
    std::cout << "---------------------------------------------------------" << std::endl << std::endl;

    //std::cout << "C API: " << std::endl;
    //simple_test_c_mpi();
    //std::cout << std::endl;

    //std::cout << "Boost.MPI: " << std::endl;
    //simple_boost_mpi(argc, argv);
    //std::cout << std::endl;

    long iterations = 1e9;
    ComputePi compute_pi = ComputePi(iterations);
    compute_pi.calculate_pi();

    MPI_Finalize();

    return 0;
}

