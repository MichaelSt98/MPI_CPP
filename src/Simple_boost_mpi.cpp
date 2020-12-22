
#include "../include/Simple_boost_mpi.h"

namespace mpi = boost::mpi;

void simple_boost_mpi(int argc, char** argv) {


    boost::mpi::environment env{argc, argv};
    boost::mpi::communicator world;
    std::cout << world.rank() << ", " << world.size() << '\n';

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