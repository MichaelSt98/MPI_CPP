#ifndef MPI_CPP_SIMPLE_BOOST_MPI_H
#define MPI_CPP_SIMPLE_BOOST_MPI_H

#include <boost/mpi.hpp>
#include <iostream>
#include <boost/serialization/string.hpp> // Needed to send/receive strings!

void simple_boost_mpi(int argc, char** argv);

#endif //MPI_CPP_SIMPLE_BOOST_MPI_H
