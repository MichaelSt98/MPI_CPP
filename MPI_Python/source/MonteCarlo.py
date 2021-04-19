from mpi4py import MPI
import numpy as np


class MonteCarlo:

    def __init__(self, use_mpi=True, reduced_temperature=0.9, reduced_density=0.9, n_steps=10000, freq=1000,
                 num_particles=100, simulation_cutoff=3.0, max_displacement=0.1, tune_displacement=0.1,
                 plot=True, build_method='random'):

        self.use_mpi = use_mpi

        self.world_comm = MPI.COMM_WORLD
        self.world_size = self.world_comm.Get_size()
        self.rank = self.world_comm.Get_rank()

        #else:
         #   self.rank = None

        self.reduced_temperature = reduced_temperature
        self.reduced_density = reduced_density
        self.n_steps = n_steps
        self.freq = freq
        self.num_particles = num_particles
        self.simulation_cutoff = simulation_cutoff
        self.max_displacement = max_displacement
        self.tune_displacement = tune_displacement
        self.plot = plot
        self.build_method = build_method

        self.box_length = np.cbrt(self.num_particles / self.reduced_density)
        self.beta = 1.0 / self.reduced_temperature
        self.simulation_cutoff2 = np.power(self.simulation_cutoff, 2)
        self.n_trials = 0
        self.n_accept = 0
        self.energy_array = np.zeros(n_steps)

    def main(self):

        if self.rank == 0:
            print("")
            if self.use_mpi:
                print("Start Monte Carlo simulation using MPI ...")
            else:
                print("Start Monte Carlo simulation ...")
            print("-----------------------------------------------------------")

        start_simulation_time = MPI.Wtime()
        total_energy_time = 0.0
        total_decision_time = 0.0

        if self.use_mpi:
            if self.rank == 0:
                coordinates = self.generate_initial_state(method=self.build_method)
            else:
                coordinates = np.empty([self.num_particles, 3])
            self.world_comm.Bcast([coordinates, MPI.DOUBLE], root=0)
        else:
            coordinates = self.generate_initial_state(method=self.build_method)

        total_pair_energy = self.calculate_total_pair_energy(coordinates)
        tail_correction = self.calculate_tail_correction()

        n_trials = 0

        if self.use_mpi:
            for i_step in range(self.n_steps):

                if self.rank == 0:
                    n_trials += 1

                    #np.random.seed(11)
                    i_particle = np.random.randint(self.num_particles)
                    i_particle_buf = np.array([i_particle], 'i')

                    random_displacement = (2.0 * np.random.rand(3) - 1.0) * self.max_displacement
                else:
                    i_particle_buf = np.empty(1, 'i')
                    random_displacement = np.empty(3)

                self.world_comm.Bcast([i_particle_buf, MPI.INT], root=0)
                i_particle = i_particle_buf[0]
                self.world_comm.Bcast([random_displacement, MPI.DOUBLE], root=0)
                self.world_comm.Bcast([coordinates, MPI.DOUBLE], root=0)

                start_energy_time = MPI.Wtime()
                current_energy = self.get_particle_energy(coordinates, i_particle)
                total_energy_time += MPI.Wtime() - start_energy_time

                proposed_coordinates = coordinates.copy()
                proposed_coordinates[i_particle] += random_displacement
                proposed_coordinates -= self.box_length * np.round(proposed_coordinates / self.box_length)

                start_energy_time = MPI.Wtime()
                proposed_energy = self.get_particle_energy(proposed_coordinates, i_particle)
                total_energy_time += MPI.Wtime() - start_energy_time

                if self.rank == 0:
                    start_decision_time = MPI.Wtime()

                    delta_e = proposed_energy - current_energy

                    accept = self.accept_or_reject(delta_e, self.beta)

                    if accept:
                        total_pair_energy += delta_e
                        self.n_accept += 1
                        coordinates[i_particle] += random_displacement

                    total_energy = (total_pair_energy + tail_correction) / self.num_particles

                    self.energy_array[i_step] = total_energy

                    # if True:
                    if np.mod(i_step + 1, self.freq) == 0:
                        if self.rank == 0:
                            print(i_step + 1, self.energy_array[i_step])

                        if self.tune_displacement:
                            max_displacement, n_trials, self.n_accept = self.adjust_displacement(n_trials)

                    total_decision_time += MPI.Wtime() - start_decision_time

        else:
            for i_step in range(self.n_steps):

                n_trials += 1

                #np.random.seed(11)
                i_particle = np.random.randint(self.num_particles)

                random_displacement = (2.0 * np.random.rand(3) - 1.0) * self.max_displacement

                start_energy_time = MPI.Wtime()
                current_energy = self.get_particle_energy(coordinates, i_particle)
                total_energy_time += MPI.Wtime() - start_energy_time

                proposed_coordinates = coordinates.copy()
                proposed_coordinates[i_particle] += random_displacement
                proposed_coordinates -= self.box_length * np.round(proposed_coordinates / self.box_length)

                start_energy_time = MPI.Wtime()
                proposed_energy = self.get_particle_energy(proposed_coordinates, i_particle)
                total_energy_time += MPI.Wtime() - start_energy_time

                start_decision_time = MPI.Wtime()

                delta_e = proposed_energy - current_energy

                accept = self.accept_or_reject(delta_e, self.beta)

                if accept:
                    total_pair_energy += delta_e
                    self.n_accept += 1
                    coordinates[i_particle] += random_displacement

                total_energy = (total_pair_energy + tail_correction) / self.num_particles

                self.energy_array[i_step] = total_energy

                # if True:
                if np.mod(i_step + 1, self.freq) == 0:
                    if self.rank == 0:
                        print(i_step + 1, self.energy_array[i_step])

                    if self.tune_displacement:
                        max_displacement, n_trials, self.n_accept = self.adjust_displacement(n_trials)

                total_decision_time += MPI.Wtime() - start_decision_time

        if self.rank == 0:
            print("Total simulation time: " + str(MPI.Wtime() - start_simulation_time))
            print("    Energy time:       " + str(total_energy_time))
            print("    Decision time:     " + str(total_decision_time))
            print("-----------------------------------------------------------")


    def generate_initial_state(self, method='random'):
        """
        Function generates initial coordinates for a LJ fluid simulation
        This function can generate from a random configuration
        """

        if method is 'random':

            np.random.seed(seed=1)
            coordinates = (0.5 - np.random.rand(self.num_particles, 3)) * self.box_length

        return coordinates


    def lennard_jones_potential(self, rij2):
        """
        Function evaluates the unitless LJ potential given a squared distance
        Parameters
        """
        # This function computes the LJ energy between two particles

        sig_by_r6 = np.power(1 / rij2, 3)
        sig_by_r12 = np.power(sig_by_r6, 2)
        return 4.0 * (sig_by_r12 - sig_by_r6)

    def calculate_tail_correction(self):
        """
        This function computes the standard tail energy correction for the LJ potential
        Parameters
        """

        volume = np.power(self.box_length, 3)
        sig_by_cutoff3 = np.power(1.0 / self.simulation_cutoff, 3)
        sig_by_cutoff9 = np.power(sig_by_cutoff3, 3)
        e_correction = sig_by_cutoff9 - 3.0 * sig_by_cutoff3

        e_correction *= 8.0 / 9.0 * np.pi * self.num_particles / volume * self.num_particles

        return e_correction

    def minimum_image_distance(self, r_i, r_j):
        # This function computes the minimum image distance between two particles

        rij = r_i - r_j
        rij = rij - self.box_length * np.round(rij / self.box_length)
        rij2 = np.dot(rij, rij)
        return rij2

    def get_particle_energy(self, coordinates, i_particle):
        """
        This function computes the minimum image distance between two particles
        Parameters
        """

        e_total = 0.0

        i_position = coordinates[i_particle]

        particle_count = len(coordinates)

        if self.use_mpi:
            for j_particle in range(self.rank, particle_count, self.world_size):

                if i_particle != j_particle:

                    j_position = coordinates[j_particle]

                    rij2 = self.minimum_image_distance(i_position, j_position)

                    if rij2 < self.simulation_cutoff2:
                        e_pair = self.lennard_jones_potential(rij2)
                        e_total += e_pair

            # Sum the energy across all ranks
            e_single = np.array([e_total])
            e_summed = np.zeros(1)
            self.world_comm.Allreduce([e_single, MPI.DOUBLE], [e_summed, MPI.DOUBLE], op=MPI.SUM)

            return e_summed[0]

        else:
            for j_particle in range(particle_count):
                if i_particle != j_particle:

                    j_position = coordinates[j_particle]

                    rij2 = self.minimum_image_distance(i_position, j_position)

                    if rij2 < self.simulation_cutoff2:
                        e_pair = self.lennard_jones_potential(rij2)
                        e_total += e_pair

            return e_total

    def calculate_total_pair_energy(self, coordinates):
        e_total = 0.0
        particle_count = len(coordinates)

        for i_particle in range(particle_count):
            for j_particle in range(i_particle):

                r_i = coordinates[i_particle]
                r_j = coordinates[j_particle]
                rij2 = self.minimum_image_distance(r_i, r_j)
                if rij2 < self.simulation_cutoff2:
                    e_pair = self.lennard_jones_potential(rij2)
                    e_total += e_pair

        return e_total

    def accept_or_reject(self, delta_e, beta):
        """
        Accept or reject a move based on the energy difference and system \
        temperature.
        This function uses a random numbers to adjust the acceptance criteria.
        """
        # This function accepts or reject a move given the
        # energy difference and system temperature

        if delta_e < 0.0:
            accept = True

        else:
            random_number = np.random.rand(1)
            p_acc = np.exp(-beta * delta_e)

            if random_number < p_acc:
                accept = True
            else:
                accept = False

        return accept

    def adjust_displacement(self, n_trials):
        """
        Change the acceptance criteria to get the desired rate.
        When the acceptance rate is too high, the maximum displacement is adjusted \
         to be higher.
        When the acceptance rate is too low, the maximum displacement is \
         adjusted lower.
        """
        acc_rate = float(self.n_accept) / float(n_trials)
        if (acc_rate < 0.38):
            self.max_displacement *= 0.8

        elif (acc_rate > 0.42):
            self.max_displacement *= 1.2

        n_trials = 0
        n_accept = 0

        return self.max_displacement, n_trials, n_accept
