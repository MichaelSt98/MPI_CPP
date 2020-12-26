# MPI_CPP

**Exploring Message Passing Interface (MPI) usage with (modern) C++.**

The [Message Passing Interface (MPI)](https://de.wikipedia.org/wiki/Message_Passing_Interface) provides bindings for the C and Fortran, since the C++ bindings are removed. Threfore programmers are forced to use either the C API or rely on third-party libraries/implementations.

A communicator defines a group of processes that have the ability to communicate with another in dependence of their ranks. Communication is based on sending and receiving operations among processes. If one sender and receiver is involved, this refers to point-to-point communication. If a process need to communicate with everyone else collective communication involves all processes.
First the MPI header files need to be included ```#include <mpi.h>``` and the MPI environment must be initialized with

```cpp
MPI_Init(int* argc, char*** argv)
```

constructing all of MPI’s global and internal variables. After that

```cpp
MPI_Comm_size(MPI_Comm communicator, int* size)
```

returns the size of a communicator and

```cpp
MPI_Comm_rank(MPI_Comm communicator, int* rank)
```

returns the rank of a process in a communicator. The ranks of the processes are (primarily) used for identification purposes when sending and receiving messages.
Using

```cpp
MPI_Get_processor_name(char* name, int* name_length)
```

gives the actual name of the processor on which the process is executing. The final call is

```cpp
MPI_Finalize()
```

used to clean up the MPI environment and no more MPI calls can be done afterwards.

## Compiling

using 

```bash
mpic++ mpi_file.cpp -o mpi_file
```
for compiling C++ files using MPI and 

```bash
mpirun -np 2 mpi_runner
```
for running the script.


Related compilers/scripts:

* ```mpic++```
* ```mpicc```
* ```mpichversion```
* ```mpicxx```
* ```mpiexec```
* ```mpiexec.hydra```
* ```mpif77```
* ```mpif90```
* ```mpifort```
* ```mpioutil```
* ```mpirun```
* ```mpivars```

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
