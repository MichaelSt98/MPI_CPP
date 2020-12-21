# MPI_CPP

Exploring Message Passing Interface (MPI) usage with (modern) C++.

The [Message Passing Interface (MPI)](https://de.wikipedia.org/wiki/Message_Passing_Interface) provides bindings for the C and Fortran, since the C++ bindings are removed. Threfore programmers are forced to use either the C API or rely on third-party libraries/implementations.

## TODO

* explore implementations
* explore best practice with C++
* learn MPI
* ...

## Open MPI

* [Open MPI v4 documentation](https://www.open-mpi.org/doc/v4.0/)
* [How to MPI](https://hpc-wiki.info/hpc/How_to_Use_MPI)

## Implementations

In order to use MPI the C bindings can be used, either directly or by wrapping it into a C++ class.

### Boost.MPI

* [Documentation Boost.MPI](https://www.boost.org/doc/libs/1_64_0/doc/html/mpi.html)
* [Implementation (GitHub)](https://github.com/boostorg/mpi)


### OOMPI

* [Publication: Object Oriented MPI (OOMPI): A C++ Class Library for MPI Version 1.0.3](https://www.researchgate.net/publication/2801121_Object_Oriented_MPI_OOMPI_A_C_Class_Library_for_MPI_Version_103)


### MPP

* [Publication: A lightweight C Interface to MPI](https://www.researchgate.net/publication/216836687_A_Lightweight_C_Interface_to_MPI)
* [Implementation (GitHub)](https://github.com/motonacciu/mpp)


Further, having a look at:

* [Caffe-MPI](https://github.com/Caffe-MPI/Caffe-MPI.github.io)
* [MPIO](https://github.com/frsyuki/mpio)
* [TorchMPI](https://github.com/facebookarchive/TorchMPI)
* [MPIPlatform](https://github.com/slowbull/MPIPlatform)
* [TIMPI](https://github.com/libMesh/TIMPI)

## Examples

* [MPI and OpenMP examples](https://github.com/kcherenkov/Parallel-Programming-Labs)
* [Boost.MPI examples](https://github.com/boostorg/mpi/tree/develop/example)
