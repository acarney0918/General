"""
dump.lammpstrj file to calculating RDF via python commands
"""


import numpy as np
import matplotlib.pyplot as plt

file_path = '/Users/dubay_lab/Desktop/Finite_Size_Diffusion/lammps_bootcamp/lj_fluids/msd_lj_fluids/dump.lammpstrj' 

def read_lammpstrj(file_path):
   # dump has crxn and time step values with the .lammpstrj 
    with open(file_path, 'r') as f:
        lines = f.readlines()
#read this as
    timestep_indices = [i for i, line in enumerate(lines) if 'ITEM: TIMESTEP' in line]
    num_particles = int(lines[timestep_indices[0] + 3]) #which index is time step in the row

    positions = [] # getting particle positions from the x y z portions of the index
    for i, timestep_index in enumerate(timestep_indices):
        timestep_positions = np.zeros((num_particles, 3))
        for j in range(timestep_index + 9, timestep_index + 9 + num_particles):
            particle_data = lines[j].split()
            position = [float(p) for p in particle_data[2:5]]  # with x y z cxn
            timestep_positions[int(particle_data[0]) - 1] = position
        positions.append(timestep_positions)

    return np.array(positions)

def calculate_distance(positions):
   # change in particle positions of time steps aka distance b/w neighbors
    num_timesteps, num_particles, num_dimensions = positions.shape
    distances = []

    for timestep_pos in positions:
        dists = []
        for i in range(num_particles):
            for j in range(i + 1, num_particles):
                dist = np.linalg.norm(timestep_pos[i] - timestep_pos[j])
                dists.append(dist)
        distances.append(dists)

    return np.array(distances)

def calculate_rdf(distances, dr, r_max):
   # radial distribution function
    num_timesteps, num_pairs = distances.shape
    r_values = np.arange(0, r_max, dr)
    rdf_values = np.zeros_like(r_values)

    for dists in distances:
        for dist in dists:
            if dist < r_max:
                rdf_values[int(dist // dr)] += 2  #  two RDF counts b/c its a pair of neighboring atoms

    # volume of solvation shell (lj FLUID)
    shell_volume = 4/3 * np.pi * ((r_values + dr)**3 - r_values**3)

    # Normalize RDF by dividing by shell volume
    rdf_values /= shell_volume

    return r_values, rdf_values

# dump file particle positions
positions_data = read_lammpstrj(file_path)

# pair distances between particles
distances_data = calculate_distance(positions_data)

r_values, rdf_values = calculate_rdf(distances_data, dr=0.1, r_max=10.0) #calculate rdf

# Plot RDF
plt.plot(r_values, rdf_values)
plt.xlabel('r')
plt.ylabel('g(r)')
plt.title('Radial Distribution Function (RDF)')
plt.show()
