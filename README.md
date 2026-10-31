# Parametric Bahtinov Mask Generator for FreeCAD (AI-Assisted Engineering)

An automated, production-ready Python tool for FreeCAD designed to procedurally generate a seamless **Bahtinov diffraction mask** tailored specifically for the **Sky-Watcher SkyMax 127T (Maksutov-Cassegrain)** telescope. 

This project showcases mechanical CAD automation, Python scripting within internal geometric kernels, mathematical modeling of optical diffraction, and technical documentation engineering.

> 🌟 **Note on Development:** This repository is a product of AI-Assisted Engineering. The full workflow—including mathematical verification, structural CAD optimization within the OpenCASCADE kernel, and LaTeX report compiling—was co-developed through an interactive collaboration between the engineer and an AI assistant.

---

## 🔭 Technical Specifications (SkyMax 127T)

- **Clear Aperture ($D$):** 127 mm
- **Focal Length ($F$):** 1500 mm
- **Focal Ratio:** f/11.8
- **Central Obstruction ($D_{obs}$):** 45 mm (Secondary mirror housing clearance)
- **Calculated Grating Pitch ($p$):** ~8.8 mm (Based on the empirical $F / 170$ Bahtinov formula)
- **Slot Width:** ~4.4 mm

---

## 🛠️ Key Engineering Features

1. **Procedural Geometry Generation:** Dynamically maps diffraction slots using variable parameters instead of hardcoded CAD constraints.
2. **Structural Reinforcement (Central Bridge):** Features a 6.0 mm horizontal stabilization bridge that integrates individual blade clusters. This enhances mechanical durability during FDM 3D printing and everyday field operation.
3. **Topology Optimization:** Utilizes `Part.removeSplitter()` to eliminate coplanar boundary shims inside the OpenCASCADE kernel, creating a single, clean, manifold solid body.
4. **Automated Export Pipelines:** Generates native files alongside production industrial exports simultaneously.

---

## 📂 Project Structure

- `bahtinov_generator.py` — The core Python macro utilizing the FreeCAD `Part` module to build the clean 3D solid geometry and execute automated exports.
- `bahtinov_report.tex` — A comprehensive academic/technical report written in LaTeX, detailings the underlying optical physics, Fraunhofer diffraction principles, and computational architecture.
- `Bahtinov_SkyMax127.FCStd` — Native FreeCAD project file for manual editing.
- `Bahtinov_SkyMax127.step` — Standardized high-fidelity solid CAD exchange format for universal editing or CNC/laser workflows.
- `Bahtinov_SkyMax127.stl` — Production polygonal mesh optimized for FDM slicing engines (Cura, PrusaSlicer, Bambu Studio).

---

## 🚀 How to Run and Edit

### Running the Python Automation
1. Launch **FreeCAD**.
2. Go to the top text menu: `Macro` -> `Macros...` -> Click **Create** and name it `BahtinovGenerator`.
3. Paste the contents of `bahtinov_generator.py` into the integrated editor.
4. Press `Ctrl + F6` (or `Macro -> Execute macro`) to render the geometry. 

### Manual Interface Editing
If you wish to modify the 3D model manually without Python:
1. Open `Bahtinov_SkyMax127.step` via `File -> Import`.
2. Switch to the **Part Workbench**.
3. Select the object in the Combo View tree, and navigate to `Part -> Create a copy -> Refine shape`.
4. Apply custom chamfers, mounting pins, or adjustment slots using standard UI tools.

---

## 🔬 Optical Physics Background

The mask operates on the principle of **Fraunhofer diffraction grids**. Each linear slot edge acts as a wave-front splitter, generating a fine diffraction spike perpendicular to the orientation of the slot:
- **Vertical slots** project a **horizontal** line.
- **Angled slots ($\pm20^\circ$)** project an **X-shaped** pattern.

When the star is in perfect focus, the horizontal line passes exactly through the intersection point of the "X". The mathematical grid period constraint ($p \approx F/170$) ensures optimal spike length, spatial frequency, and light intensity inside the visible spectrum ($\lambda \approx 550 \text{ nm}$) on modern astrophotography CMOS sensors.

The added horizontal mechanical bridge acts as an unslotted obstruction, projecting a very faint vertical diffraction spike. This turns the central marker into a stable crosshair, which further assists visual focus estimation without changing the focal calculations.

---

## 🤖 AI Collaboration Insights

The architecture of this project leverages modern AI pair-programming techniques to solve complex topological constraints in open-source CAD software:
- **Kernel-level problem solving:** The AI assisted in bypassing OpenCASCADE segmentation issues by re-architecting the boolean subtraction sequence, ensuring a smooth, single-body result without artifact shims.
- **Cross-disciplinary translation:** The workflow allowed for instant synchronization between mathematical optical equations, FreeCAD Python API bindings, and strict LaTeX academic document layouts.
