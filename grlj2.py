import matplotlib
matplotlib.use('Agg')

import numpy as np
import matplotlib.pyplot as plt


file_path = ('/Users/dubay_lab/Desktop/Finite_Size_Diffusion/lammps_bootcamp/lj_fluids/Take_2/rdf_output_and.dat')

def load_dat_file(file_path):
    # Open the file and read lines, starting from the fourth line
    with open(file_path, 'r') as f:
        lines = f.readlines()[3:]

    # Initialize empty lists to store data
    x_data = []
    y_data = [[] for _ in range(3)]  # Create three empty lists for y data

    # Iterate over each line in the file
    for line in lines:
        # Split the line into columns
        columns = line.split()

        # Check if the line has at least four columns
        if len(columns) >= 3:
            # Extract data from columns
            x_data.append(float(columns[0]))
            for i in range(3):  # Extract y data for each column
                y_data[i].append(float(columns[i + 1]))

    # Convert lists to numpy arrays
    x = np.array(x_data)
    y = [np.array(data) for data in y_data]

    return x, y

def plot_dat_file(file_path):
    # Load data from the .dat file
    x, y = load_dat_file(file_path)

    # Plot the data
    fig, axs = plt.subplots(3, 1, figsize=(8, 6), sharex=True)

    for i in range(3):
        axs[i].scatter(x, y[i], label=f'Y{i+1} Data')
        axs[i].set_ylabel(f'Y{i+1}')  # Set y-axis label for each subplot

    plt.xlabel('X Axis Label')  # Replace with your desired label for x-axis
    plt.suptitle('Title of the Plot')  # Replace with your desired title
    plt.subplots_adjust(hspace=0.3)  # Adjust vertical spacing between subplots
    plt.savefig('grlj3.png')
    plt.show()

# Example usage:
# file_path = 'your_data_file.dat'  # Replace with the path to your .dat file
# plot_dat_file(file_path)
