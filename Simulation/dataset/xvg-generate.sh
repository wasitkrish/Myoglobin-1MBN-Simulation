#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

BASE="$PROJECT_ROOT/files"
OUT="$PROJECT_ROOT/dataset/xvgdata"

TPR="$BASE/md.tpr"
XTC="$BASE/md.xtc"
EDR="$BASE/md.edr"

DT=10
mkdir -p "$OUT"

echo "===== TRAJECTORY PROPERTIES (10 ps) ====="

# RMSD (Backbone vs Backbone)
printf "Backbone\nBackbone\n" | gmx rms \
    -s "$TPR" -f "$XTC" \
    -o "$OUT/rmsd.xvg" \
    -dt $DT -tu ns

# RMSF (per residue)
echo "Protein" | gmx rmsf \
    -s "$TPR" -f "$XTC" \
    -o "$OUT/rmsf.xvg" \
    -res -dt $DT

# Radius of Gyration
echo "Protein" | gmx gyrate \
    -s "$TPR" -f "$XTC" \
    -o "$OUT/gyrate.xvg" \
    -dt $DT

# SASA
echo "Protein" | gmx sasa \
    -s "$TPR" -f "$XTC" \
    -o "$OUT/sasa.xvg" \
    -dt $DT

# H-bonds
printf "Protein\nProtein\n" | gmx hbond \
    -s "$TPR" -f "$XTC" \
    -num "$OUT/hbond.xvg" \
    -dt $DT

# DSSP (secondary structure)
gmx do_dssp \
    -s "$TPR" -f "$XTC" \
    -o "$OUT/dssp.xpm" \
    -sc "$OUT/dssp_num.xvg" \
    -dt $DT

echo "===== ENERGY TERMS (native resolution) ====="

echo "Potential"     | gmx energy -f "$EDR" -o "$OUT/potential.xvg"
echo "Total-Energy"  | gmx energy -f "$EDR" -o "$OUT/total_energy.xvg"
echo "Kinetic-En."   | gmx energy -f "$EDR" -o "$OUT/kinetic_energy.xvg"
echo "Temperature"   | gmx energy -f "$EDR" -o "$OUT/temperature.xvg"
echo "Pressure"      | gmx energy -f "$EDR" -o "$OUT/pressure.xvg"
echo "Density"       | gmx energy -f "$EDR" -o "$OUT/density.xvg"

echo "===== ALL XVG FILES GENERATED SUCCESSFULLY ====="