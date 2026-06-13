import pandas as pd
import numpy as np
import os
from pathlib import Path

# ---------- SETTINGS ----------
script_dir = Path(__file__).resolve().parent
input_folder = script_dir / "xvgdata"
output_folder = script_dir / "output"
output_name = "myoglobin_simulation_data.xlsx"
TARGET_DT = 10  # ps
# ------------------------------

def read_xvg(file_path, column_name):
    data = []
    with open(file_path) as f:
        for line in f:
            if not line.startswith(('@', '#')):
                cols = line.split()
                if len(cols) >= 2:
                    data.append([float(cols[0]), float(cols[1])])
    return pd.DataFrame(data, columns=["time", column_name])


def detect_dt(df):
    if len(df) < 3:
        return None
    return round(np.median(np.diff(df["time"])), 3)


def resample_to_grid(df, name, target_dt):
    df = df.copy()
    df["bin"] = (df["time"] / target_dt).round().astype(int)
    df = df.groupby("bin")[name].mean().reset_index()
    df["time"] = df["bin"] * target_dt
    return df[["time", name]]


# create output directory
os.makedirs(output_folder, exist_ok=True)

files = [f for f in sorted(Path(input_folder).glob("*.xvg")) 
         if not f.name.startswith("#")]

if not files:
    raise Exception("No XVG files found in folder!")

print("\n===== Processing XVG files =====\n")

dataset = None
master_time = None

for file in files:
    name = file.stem
    print(f"Reading {file.name}")

    df = read_xvg(file, name)
    dt = detect_dt(df)
    print(f"  detected dt = {dt} ps")

    # If higher resolution than target → average
    if dt is not None and dt < TARGET_DT:
        print("  → averaging into 10 ps bins")
        df = resample_to_grid(df, name, TARGET_DT)

    df = df.sort_values("time").reset_index(drop=True)

    # Use first file as master time grid
    if dataset is None:
        master_time = df["time"].copy()
        dataset = pd.DataFrame({"time": master_time})
    
    # Align each dataset to master timeline
    dataset = dataset.merge(df, on="time", how="left")

# Interpolate missing values smoothly
dataset = dataset.sort_values("time").interpolate(limit_direction="both")

# Final cleanup
dataset = dataset.reset_index(drop=True)

# Save files
output_file = os.path.join(str(output_folder), output_name)
dataset.to_excel(output_file, index=False)
dataset.to_csv(output_file.replace(".xlsx", ".csv"), index=False)

print("\n===== Dataset created successfully! =====")
print(f"Rows: {len(dataset)}")
print(f"Columns: {len(dataset.columns)}")
print(f"Saved at: {output_file}")