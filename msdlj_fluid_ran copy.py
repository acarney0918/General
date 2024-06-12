import numpy as np
import matplotlib.pyplot as plt

file_path = '/Users/dubay_lab/Desktop/Finite_Size_Diffusion/lammps_bootcamp/lj_fluids/msd_lj_fluids/min2_dump.lammpstrj'  # Replace with the path to your .lammpstrj file
def positions(file_path):
    positions = read_lammpstrj(file_path)
    return positions  # Add this line to return the positions data

def read_lammpstrj(file_path):
    """
    Read LAMMPS trajectory file and extract particle positions.

    Parameters:
    file_path : str
        Path to the LAMMPS trajectory file.

    Returns:
    positions : numpy.ndarray
        Array of shape (num_particles, num_dimensions, num_timesteps) containing
        the particle positions over time.
    """
    with open(file_path, 'r') as f:
        lines = f.readlines()

    # Find the line numbers where the timesteps start
    timestep_indices = [i for i, line in enumerate(lines) if 'ITEM: TIMESTEP' in line]

    # Initialize lists to store particle positions
    positions_list = []
    timestep_start = 0

    for i, timestep_index in enumerate(timestep_indices):
        # Find the number of particles and skip header lines
        num_particles = int(lines[timestep_index + 3])

        # Extract particle positions
        timestep_positions = []
        for j in range(timestep_index + 9, timestep_index + 9 + num_particles):
            particle_data = lines[j].split()
            position = [float(p) for p in particle_data[2:5]]  # Assuming x, y, z coordinates
            timestep_positions.append(position)

        positions_list.append(timestep_positions)

    # Convert positions list to numpy array
    positions = np.array(positions_list)

    return positions

def mean_square_displacement(positions):
    """
    Calculate the mean square displacement (MSD) of a set of particle trajectories.

    Parameters:
    positions : numpy.ndarray
        Array of shape (num_particles, num_dimensions, num_timesteps) containing
        the particle positions over time.

    Returns:
    msd : numpy.ndarray
        Array containing the MSD for each timestep.
    """
    num_particles, num_dims, num_timesteps = positions.shape
    msd = np.zeros(num_timesteps)

    for t in range(1, num_timesteps):
        displacement = positions[:, :, t] - positions[:, :, 0]
        msd[t] = np.mean(np.sum(displacement**2, axis=1))

    return msd

# Example usage:
file_path = '/Users/dubay_lab/Desktop/Finite_Size_Diffusion/lammps_bootcamp/lj_fluids/msd_lj_fluids/min2_dump.lammpstrj'  # Replace with the path to your .lammpstrj file

# Calculate the mean square displacement
msd = mean_square_displacement(positions(file_path))

# Plot MSD over time
plt.plot(msd)
plt.xlabel('Time')
plt.ylabel('Mean Square Displacement')
plt.title('Mean Square Displacement vs Time')
plt.show()
