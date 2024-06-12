import numpy as np
import matplotlib.pyplot as plt
import matplotlib

file_path = ('/Users/dubay_lab/Desktop/lj_fluids/Lattice/rdf_output_lattice.dat')
# print(file_path)

matplotlib.use('TkAgg')

def load_dat_file(file_path):
    # Load data from the .dat file
    data = np.loadtxt(file_path)
    x = data[:, 0]  # First column (r)
    y = data[:, 1]  # Second column (g(r))
    return x, y

def plot_ke(file_path):
    # Load data from the .dat file
    x, y = load_dat_file(file_path)

    # Plot the RDF
    plt.figure(figsize=(8, 6))
    plt.plot(x, y, label='KE')
    plt.xlabel('Timestep')
    plt.ylabel('Kinetic Energy')
    plt.title('Kinetic Energy vs Timestep NPT')
    plt.show()
    plt.savefig('energy_npt.png')

plot_ke(file_path)

# Example usage:
# file_path = 'your_data_file.dat'  # Replace with the path to your .dat file
# plot_rdf(file_path)
