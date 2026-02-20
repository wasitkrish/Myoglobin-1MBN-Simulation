import numpy as np
import matplotlib.pyplot as plt
import os

def read_xvg(filename):
    data = []
    legends = []
    title = ""
    xlabel = ""
    ylabel = ""

    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()

            # Skip comments
            if line.startswith('#'):
                continue

            # Extract metadata safely
            if line.startswith('@'):
                if "title" in line and '"' in line:
                    title = line.split('"')[1]

                elif "xaxis" in line and '"' in line:
                    xlabel = line.split('"')[1]

                elif "yaxis" in line and '"' in line:
                    ylabel = line.split('"')[1]

                elif "legend" in line and '"' in line:
                    legends.append(line.split('"')[1])

                continue

            # Read numerical data
            if line:
                data.append([float(x) for x in line.split()])

    return np.array(data), title, xlabel, ylabel, legends


# ===== Main Program =====

filename = "/home/krish/Desktop/Material-Informatics/MD Simulation/Myoglobin 1MBN notebook/gyrate.xvg"

data, title, xlabel, ylabel, legends = read_xvg(filename)

time = data[:, 0]
rg_total = data[:, 1]

plt.figure(figsize=(10, 6))

# Plot total Rg
plt.plot(time, rg_total, label="Rg", linewidth=2)

# If components exist (X, Y, Z)
if data.shape[1] > 2:
    plt.plot(time, data[:, 2], label="Rg/sX/N", linewidth=1.5)

if data.shape[1] > 3:
    plt.plot(time, data[:, 3], label="Rg/sY/N", linewidth=1.5)

if data.shape[1] > 4:
    plt.plot(time, data[:, 4], label="Rg/sZ/N", linewidth=1.5)

plt.title(title if title else "Radius of Gyration (Total and Around Axes)", fontsize=14)
plt.xlabel(xlabel if xlabel else "Time (ps)", fontsize=12)
plt.ylabel(ylabel if ylabel else "Radius (nm)", fontsize=12)

# Legend outside
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))

plt.tight_layout(rect=[0, 0, 0.85, 1])

# ===== Save Plot =====
output_folder = "plots"

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

output_path ="/home/krish/Desktop/Material-Informatics/MD Simulation/Myoglobin 1MBN notebook/graphs/plots/gyrate_multi.png"
plt.savefig(output_path, dpi=300)

print(f"Plot saved at: {output_path}")

plt.show()