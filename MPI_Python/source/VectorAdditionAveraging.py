import numpy as np
from mpi4py import MPI

class VectorAdditionAveraging:

    def __init__(self, N = 100000):
        self.N = N
        self.world_comm = MPI.COMM_WORLD
        self.world_size = self.world_comm.Get_size()
        self.rank = self.world_comm.Get_rank()

    def without_communication(self):
        if self.rank == 0:
            print("")
            print("Working with arrays without communication")
            print("----------------------------------------------------")

        # determine the workload of each rank
        workloads = [ self.N // self.world_size for i in range(self.world_size) ]
        for i in range( self.N % self.world_size ):
            workloads[i] += 1
        my_start = 0
        for i in range( self.rank ):
            my_start += workloads[i]
        my_end = my_start + workloads[self.rank]

        # initialize a
        start_time = MPI.Wtime()
        a = np.ones( self.N )
        end_time = MPI.Wtime()
        if self.rank == 0:
            print("Initialize a time: " + str(end_time - start_time))

        # initialize b
        start_time = MPI.Wtime()
        b = np.zeros( self.N )
        for i in range( self.N ):
            b[i] = 1.0 + i
        end_time = MPI.Wtime()
        if self.rank == 0:
            print("Initialize b time: " + str(end_time - start_time))

        # add the two arrays
        start_time = MPI.Wtime()
        for i in range( self.N ):
            a[i] = a[i] + b[i]
        end_time = MPI.Wtime()
        if self.rank == 0:
            print("Add arrays time: " + str(end_time - start_time))

        # average the result
        start_time = MPI.Wtime()
        sum = 0.0
        for i in range( self.N ):
            sum += a[i]
        average = sum / self.N
        end_time = MPI.Wtime()
        if self.rank == 0:
            print("Average result time: " + str(end_time - start_time))
            print("Average: " + str(average))


    def point_to_point_communication(self):
        if self.rank == 0:
            print("")
            print("Working with arrays with point to point communication")
            print("----------------------------------------------------")

        # determine the workload of each rank
        workloads = [ self.N // self.world_size for i in range(self.world_size) ]
        for i in range( self.N % self.world_size ):
            workloads[i] += 1
        my_start = 0
        for i in range( self.rank ):
            my_start += workloads[i]
        my_end = my_start + workloads[self.rank]

        # initialize a
        start_time = MPI.Wtime()
        a = np.ones( self.N )
        end_time = MPI.Wtime()
        if self.rank == 0:
            print("Initialize a time: " + str(end_time -start_time))

        # initialize b
        start_time = MPI.Wtime()
        b = np.zeros( self.N )
        for i in range(my_start, my_end):
            b[i] = 1.0 + i
        end_time = MPI.Wtime()
        if self.rank == 0:
            print("Initialize b time: " + str(end_time -start_time))

        # add the two arrays
        start_time = MPI.Wtime()
        for i in range(my_start, my_end):
            a[i] = a[i] + b[i]
        end_time = MPI.Wtime()
        if self.rank == 0:
            print("Add arrays time: " + str(end_time -start_time))

        # average the result
        start_time = MPI.Wtime()
        sum = 0.0
        for i in range(my_start, my_end):
            sum += a[i]

        if self.rank == 0:
            world_sum = sum
            for i in range( 1, self.world_size ):
                sum_np = np.empty( 1 )
                self.world_comm.Recv( [sum_np, MPI.DOUBLE], source=i, tag=77 )
                world_sum += sum_np[0]
            average = world_sum / self.N
        else:
            sum_np = np.array( [sum] )
            self.world_comm.Send( [sum_np, MPI.DOUBLE], dest=0, tag=77 )

        end_time = MPI.Wtime()
        if self.rank == 0:
            print("Average result time: " + str(end_time -start_time))
            print("Average: " + str(average))


    def reducing_memory_footprint(self):
        if self.rank == 0:
            print("")
            print("Reducing memory footprint")
            print("----------------------------------------------------")

        # determine the workload of each rank
        workloads = [ self.N // self.world_size for i in range(self.world_size) ]
        for i in range( self.N % self.world_size ):
            workloads[i] += 1
        my_start = 0
        for i in range( self.rank ):
            my_start += workloads[i]
        my_end = my_start + workloads[self.rank]

        # initialize a
        start_time = MPI.Wtime()
        a = np.ones( workloads[self.rank] )
        end_time = MPI.Wtime()
        if self.rank == 0:
            print("Initialize a time: " + str(end_time - start_time))

        # initialize b
        start_time = MPI.Wtime()
        b = np.zeros( workloads[self.rank] )
        for i in range( workloads[self.rank]):
            b[i] = 1.0 + ( i + my_start )
        end_time = MPI.Wtime()
        if self.rank == 0:
            print("Initialize b time: " + str(end_time - start_time))

        # add the two arrays
        start_time = MPI.Wtime()
        for i in range( workloads[self.rank] ):
            a[i] = a[i] + b[i]
        end_time = MPI.Wtime()
        if self.rank == 0:
            print("Add arrays time: " + str(end_time - start_time))

        # average the result
        start_time = MPI.Wtime()
        sum = 0.0
        for i in range( workloads[self.rank] ):
            sum += a[i]

        if self.rank == 0:
            world_sum = sum
            for i in range( 1, self.world_size ):
                sum_np = np.empty( 1 )
                self.world_comm.Recv( [sum_np, MPI.DOUBLE], source=i, tag=77 )
                world_sum += sum_np[0]
            average = world_sum / self.N
        else:
            sum_np = np.array( [sum] )
            self.world_comm.Send( [sum_np, MPI.DOUBLE], dest=0, tag=77 )

        end_time = MPI.Wtime()
        if self.rank == 0:
            print("Average result time: " + str(end_time - start_time))
            print("Average: " + str(average))

    def collective_communication(self):
        if self.rank == 0:
            print("")
            print("Collective communication")
            print("----------------------------------------------------")

        # determine the workload of each rank
        workloads = [self.N // self.world_size for i in range(self.world_size)]
        for i in range(self.N % self.world_size):
            workloads[i] += 1
        my_start = 0
        for i in range(self.rank):
            my_start += workloads[i]
        my_end = my_start + workloads[self.rank]

        # initialize a
        start_time = MPI.Wtime()
        a = np.ones(workloads[self.rank])
        end_time = MPI.Wtime()
        if self.rank == 0:
            print("Initialize a time: " + str(end_time - start_time))

        # initialize b
        start_time = MPI.Wtime()
        b = np.zeros(workloads[self.rank])
        for i in range(workloads[self.rank]):
            b[i] = 1.0 + (i + my_start)
        end_time = MPI.Wtime()
        if self.rank == 0:
            print("Initialize b time: " + str(end_time - start_time))

        # add the two arrays
        start_time = MPI.Wtime()
        for i in range(workloads[self.rank]):
            a[i] = a[i] + b[i]
        end_time = MPI.Wtime()
        if self.rank == 0:
            print("Add arrays time: " + str(end_time - start_time))

        # average the result
        start_time = MPI.Wtime()
        sum = 0.0
        for i in range(workloads[self.rank]):
            sum += a[i]

        sum = np.array([sum])
        world_sum = np.zeros(1)
        self.world_comm.Reduce([sum, MPI.DOUBLE], [world_sum, MPI.DOUBLE], op=MPI.SUM, root=0)
        average = world_sum / self.N

        end_time = MPI.Wtime()
        if self.rank == 0:
            print("Average result time: " + str(end_time - start_time))
            print("Average: " + str(average[0]))