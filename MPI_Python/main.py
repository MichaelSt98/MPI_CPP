from mpi4py import MPI
from source.VectorAdditionAveraging import VectorAdditionAveraging
from source.MonteCarlo import MonteCarlo
import numpy as np

if __name__ == "__main__":

    # Simple/Basic MPI setup
    world_comm = MPI.COMM_WORLD
    world_size = world_comm.Get_size()
    rank = world_comm.Get_rank()

    print("Hello World from rank " + str(rank) + " out of " + str(world_size) + " processors.")

    # Vector addition and averaging using MPI
    vector_addition_averaging = VectorAdditionAveraging()

    vector_addition_averaging.without_communication()
    vector_addition_averaging.point_to_point_communication()
    vector_addition_averaging.point_to_point_communication()
    vector_addition_averaging.collective_communication()


    # Monte Carlo simulation using MPI
    reduced_temperature = 0.9
    reduced_density = 0.9
    n_steps = 10000#10#10000
    freq = 1000#1#1000
    num_particles = 100
    simulation_cutoff = 3.0
    max_displacement = 0.1
    tune_displacement = 0.1
    plot = True
    build_method = 'random'

    monte_carlo = MonteCarlo(use_mpi=False, reduced_temperature=reduced_temperature,
                             reduced_density=reduced_density,
                             n_steps=n_steps, freq=freq, num_particles=num_particles,
                             simulation_cutoff=simulation_cutoff, max_displacement=max_displacement,
                             tune_displacement=tune_displacement, plot=plot, build_method=build_method)
    monte_carlo.main()

    monte_carlo_mpi = MonteCarlo(use_mpi=True, reduced_temperature=reduced_temperature,
                                 reduced_density=reduced_density,
                                 n_steps=n_steps, freq=freq, num_particles=num_particles,
                                 simulation_cutoff=simulation_cutoff, max_displacement=max_displacement,
                                 tune_displacement=tune_displacement, plot=plot, build_method=build_method)
    monte_carlo_mpi.main()
    




