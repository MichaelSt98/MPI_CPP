#include <iostream>
#include "../include/Simple_C_API.h"
#include "../include/Simple_boost_mpi.h"

int main(int argc, char** argv) {

    std::cout << "Exploring MPI ..." << std::endl;

    std::cout << "C API: " << std::endl;
    simple_test_c_mpi();
    std::cout << "Boost.MPI: " << std::endl;
    simple_boost_mpi(argc, argv);

    MPI_Finalize();

    return 0;
}

