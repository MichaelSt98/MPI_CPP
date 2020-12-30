
#include "../include/Simple_boost_mpi.h"

namespace mpi = boost::mpi;

void simple_boost_mpi(int argc, char** argv) {


    boost::mpi::environment env{argc, argv};
    boost::mpi::communicator world;

    // Print off a hello world message
    std::cout << "Hello world from processor " << env.processor_name();
    std::cout << ", rank " << world.rank();
    std::cout << ", out of " << world.size() << " processors" << std::endl;


    /*
    mpi::environment env(argc, argv);
    mpi::communicator world;

    if (world.rank() == 0) {
        world.send(1, 0, std::string("Hello"));
        std::string msg;
        world.recv(1, 1, msg);
        std::cout << msg << "!" << std::endl;
    } else {
        std::string msg;
        world.recv(0, 0, msg);
        std::cout << msg << ", ";
        std::cout.flush();
        world.send(0, 1, std::string("world"));
    }
    */
}