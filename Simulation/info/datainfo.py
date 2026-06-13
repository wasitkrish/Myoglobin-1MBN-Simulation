import numpy as np
import pandas as pd
import MDAnalysis as mda
import matplotlib.pyplot as plt
import os
import re
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4

# ============================================
# PATHS
# ============================================

base = "/home/krish/Desktop/Material-Informatics/MD Simulation/Myoglobin 1MBN/files/"
output_dir = "/home/krish/Desktop/Material-Informatics/MD Simulation/Myoglobin 1MBN/info/data/"
os.makedirs(output_dir, exist_ok=True)

structure_file = os.path.join(base, "md.gro")

xvg_files = {
    "RMSD": (os.path.join(base, "rmsd.xvg"), "nm"),
    "RMSF": (os.path.join(base, "rmsf.xvg"), "nm"),
    "Radius of Gyration": (os.path.join(base, "gyrate.xvg"), "nm"),
    "Hydrogen Bonds": (os.path.join(base, "hbnum.xvg"), "count"),
    "Pressure": (os.path.join(base, "pressure.xvg"), "bar"),
    "Temperature": (os.path.join(base, "temperature.xvg"), "K"),
    "Potential Energy": (os.path.join(base, "potential.xvg"), "kJ/mol"),
    "Kinetic Energy": (os.path.join(base, "kinetic_energy.xvg"), "kJ/mol"),
    "Total Energy": (os.path.join(base, "total_energy.xvg"), "kJ/mol"),
    "SASA": (os.path.join(base, "sasa.xvg"), "nm^2"),
    "Density": (os.path.join(base, "density.xvg"), "kg/m^3")
}

print("\n========== MD SIMULATION REPORT ==========\n")

# ============================================
# SAFE FILENAME
# ============================================

def safe_filename(text):
    return re.sub(r"[^\w\-_\.]", "_", text)

# ============================================
# READ XVG
# ============================================

def read_xvg(file):
    if not os.path.exists(file):
        print("Missing:", file)
        return None, None
    data = np.loadtxt(file, comments=["@", "#"])
    if data.ndim == 1:
        return None, None
    return data[:, 0], data[:, 1]

# ============================================
# STRUCTURE INFO
# ============================================

u = mda.Universe(structure_file)

atoms = len(u.atoms)
residues = len(u.residues)
chains = len(u.segments)

aa_residues = [res for res in u.residues if res.resname not in ["SOL", "CL"]]
num_amino_acids = len(aa_residues)

protein_name = "Myoglobin"
protein_id = "1MBN"
net_charge = 2

print("Protein Name:", protein_name)
print("Protein ID:", protein_id)
print("Number of Chains:", chains)
print("Number of Amino Acids:", num_amino_acids)
print("Net Charge:", net_charge)

# ============================================
# XVG ANALYSIS
# ============================================

results = {}

for label, (file, unit) in xvg_files.items():

    x, y = read_xvg(file)
    if y is None:
        continue

    avg = np.mean(y)
    std = np.std(y)

    results[label + " Avg"] = f"{avg:.4f} {unit}"
    results[label + " Std"] = f"{std:.4f} {unit}"

    print(f"{label}: avg={avg:.4f} {unit}, std={std:.4f} {unit}")

    plt.figure(figsize=(6,4))
    plt.plot(x, y)
    plt.xlabel("Time (ps)")
    plt.ylabel(f"{label} ({unit})")
    plt.title(f"{label} ({unit})")
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, safe_filename(label) + ".png"), dpi=300)
    plt.close()

# ============================================
# SAVE CSV
# ============================================

report = {
    "Protein Name": protein_name,
    "Protein ID": protein_id,
    "Number of Chains": chains,
    "Number of Amino Acids": num_amino_acids,
    "Net Charge": net_charge,
    "Total Atoms": atoms
}

report.update(results)

csv_path = os.path.join(output_dir, "MD_Report.csv")
pd.DataFrame(report.items(), columns=["Property", "Value"]).to_csv(csv_path, index=False)

print("\nCSV saved at:", csv_path)

# ============================================
# SAVE FORMATTED PDF
# ============================================

pdf_path = os.path.join(output_dir, "MD_Report.pdf")

doc = SimpleDocTemplate(
    pdf_path,
    pagesize=A4,
    rightMargin=40,
    leftMargin=40,
    topMargin=40,
    bottomMargin=40
)

styles = getSampleStyleSheet()
story = []

# ===== Centered Title Style =====
title_style = ParagraphStyle(
    'CenteredTitle',
    parent=styles['Title'],
    fontSize=16,
    alignment=1,
    spaceAfter=6
)

# ===== Centered Subtitle Style =====
subtitle_style = ParagraphStyle(
    'CenteredSubtitle',
    parent=styles['Normal'],
    fontSize=9,
    textColor=colors.darkgray,
    alignment=1,
    spaceAfter=2
)

# ===== Title =====
story.append(Paragraph(
    "<b>MD Simulation Report – Myoglobin (1MBN)</b>",
    title_style
))

# ===== Project Info =====
story.append(Paragraph(
    "Project By: <b>Krish Singh (@wasitkrish)</b>",
    subtitle_style
))

story.append(Paragraph(
    '<link href="https://github.com/wasitkrish/Material-Informatics">'
    '<u><font color="blue">https://github.com/wasitkrish/Material-Informatics</font></u>'
    '</link>',
    subtitle_style
))

story.append(Spacer(1, 0.3 * inch))

# ===== Table Data =====
table_data = [["Property", "Value"]]

for k, v in report.items():
    table_data.append([str(k), str(v)])

# Create table
table = Table(table_data, colWidths=[3.2 * inch, 2.2 * inch], hAlign='CENTER')

table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 9),

    ('ALIGN', (0, 0), (0, -1), 'LEFT'),
    ('ALIGN', (1, 0), (1, -1), 'CENTER'),

    ('GRID', (0, 0), (-1, -1), 0.3, colors.grey),

    ('LEFTPADDING', (0, 0), (-1, -1), 6),
    ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ('TOPPADDING', (0, 0), (-1, -1), 3),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
]))

story.append(table)

doc.build(story)

print("PDF saved at:", pdf_path)