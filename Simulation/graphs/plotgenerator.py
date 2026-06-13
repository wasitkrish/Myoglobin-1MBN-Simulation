import os
import matplotlib.pyplot as plt
import seaborn as sns

# ===== Get script directory =====
script_dir = os.path.dirname(os.path.abspath(__file__))

# ===== Input directory (parent folder of graphs/) =====
xvg_dir = "/home/krish/Desktop/Material-Informatics/MD Simulation/Myoglobin 1MBN/files"

# ===== Output directory (same as previous programs) =====
output_dir = os.path.join(script_dir, "plots")
os.makedirs(output_dir, exist_ok=True)

print("Reading XVG files from:", xvg_dir)
print("Saving plots to:", output_dir)

# List all XVG files
xvg_files = [f for f in os.listdir(xvg_dir) if f.endswith('.xvg')]

# Seaborn style
sns.set(style="whitegrid", palette="bright", context="notebook")

# ===== Function to read XVG =====
def read_xvg(file_path):
    x, y = [], []
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith(('#', '@')):
                continue
            parts = line.split()
            if len(parts) >= 2:
                x.append(float(parts[0]))
                y.append(float(parts[1]))
    return x, y


# ===== Plot each XVG file =====
for file in xvg_files:
    file_path = os.path.join(xvg_dir, file)
    x, y = read_xvg(file_path)

    if not x:
        continue

    plt.figure(figsize=(9, 5))
    plt.plot(x, y, linewidth=1.8)

    plt.title(file, fontsize=13)
    plt.xlabel("Time (ps)")
    plt.ylabel("Value")

    plt.tight_layout()

    save_path = os.path.join(output_dir, f"{os.path.splitext(file)[0]}.png")
    plt.savefig(save_path, dpi=300)
    plt.close()

    print("Saved:", save_path)

print("\nAll plots saved successfully.")