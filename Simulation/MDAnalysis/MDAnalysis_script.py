import MDAnalysis as mda
from MDAnalysis.analysis import rms, align
from MDAnalysis.analysis.rms import RMSF
import matplotlib.pyplot as plt

# =====================================
# 1. Load Files
# =====================================

topology = "/home/krish/Desktop/Material-Informatics/MD Simulation/Myoglobin 1MBN notebook/md.gro"
trajectory = "/home/krish/Desktop/Material-Informatics/MD Simulation/Myoglobin 1MBN notebook/md.xtc"

u = mda.Universe(topology, trajectory)
protein = u.select_atoms("protein")
backbone = protein.select_atoms("backbone")

print("System Loaded Successfully")
print(u)

# =====================================
# 2. Align Trajectory
# =====================================

print("Aligning trajectory...")
align.AlignTraj(u, u, select="protein and backbone", in_memory=True).run()

# =====================================
# 3. RMSD
# =====================================

print("Calculating RMSD...")
R = rms.RMSD(u, u, select="protein and backbone", ref_frame=0)
R.run()

rmsd = R.results.rmsd
plt.figure()
plt.plot(rmsd[:,1], rmsd[:,2])
plt.xlabel("Time (ps)")
plt.ylabel("RMSD (Å)")
plt.title("Backbone RMSD")
plt.savefig("/home/krish/Desktop/Material-Informatics/MD Simulation/Myoglobin 1MBN notebook/MD Analysis/Output/RMSD.png")
plt.close()

# =====================================
# 4. RMSF
# =====================================

print("Calculating RMSF...")
rmsf = RMSF(backbone).run()

plt.figure()
plt.plot(backbone.resids, rmsf.results.rmsf)
plt.xlabel("Residue ID")
plt.ylabel("RMSF (Å)")
plt.title("Backbone RMSF")
plt.savefig("/home/krish/Desktop/Material-Informatics/MD Simulation/Myoglobin 1MBN notebook/MD Analysis/Output/RMSF.png")
plt.close()

# =====================================
# 5. Radius of Gyration
# =====================================

print("Calculating Radius of Gyration...")
rg = []
time = []

for ts in u.trajectory:
    rg.append(protein.radius_of_gyration())
    time.append(u.trajectory.time)

plt.figure()
plt.plot(time, rg)
plt.xlabel("Time (ps)")
plt.ylabel("Radius of Gyration (Å)")
plt.title("Radius of Gyration")
plt.savefig("/home/krish/Desktop/Material-Informatics/MD Simulation/Myoglobin 1MBN notebook/MD Analysis/Output/Radius_of_Gyration.png")
plt.close()