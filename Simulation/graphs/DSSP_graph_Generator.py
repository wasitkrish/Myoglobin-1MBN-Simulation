import os
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

file_path = Path(__file__).resolve().parents[1] / "files" / "dssp_num.xvg"

time = []
data = []
legends = []
title = ""
xlabel = ""
ylabel = ""

with open(file_path) as f:
    for line in f:
        line = line.strip()

        # Extract metadata safely
        if line.startswith("@"):
            if "title" in line and '"' in line:
                title = line.split('"')[1]
            elif "xaxis" in line and '"' in line:
                xlabel = line.split('"')[1]
            elif "yaxis" in line and '"' in line:
                ylabel = line.split('"')[1]
            elif line.startswith("@ s") and "legend" in line and '"' in line:
                legends.append(line.split('"')[1])
            continue

        # Skip comments
        if line.startswith("#"):
            continue

        parts = line.split()
        if len(parts) > 1:
            time.append(float(parts[0]))
            data.append([float(x) for x in parts[1:]])

time = np.array(time)
data = np.array(data)

print("Detected indices:")
for i, name in enumerate(legends):
    print(f"{i} → {name}")

# -------- Plot ALL indices --------
plt.figure(figsize=(11, 6))

for i in range(len(legends)):
    plt.plot(time, data[:, i], label=legends[i], linewidth=1.5)

plt.xlabel(xlabel if xlabel else "Time (ps)", fontsize=12)
plt.ylabel(ylabel if ylabel else "Number of Structures", fontsize=12)
plt.title(title if title else "Secondary Structure Evolution (DSSP)", fontsize=14)

plt.grid(True)

# Legend outside
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))

plt.tight_layout(rect=[0, 0, 0.85, 1])

# -------- Save Plot --------
output_folder = Path(__file__).resolve().parent / "plots"

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

output_path = output_folder / "DSSP.png"
plt.savefig(output_path, dpi=300)

print(f"\nPlot saved at: {output_path}")

plt.show()