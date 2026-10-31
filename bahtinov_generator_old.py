"""
FreeCAD Bahtinov Mask Generator Script
Optimized for: Sky-Watcher SkyMax 127T (Maksutov-Cassegrain)
Author: CAD Automation Portfolio Project

This script calculates the optimal diffraction grating profile for an aperture
using the empirical formula (pitch = F / 170) and generates a manufacturing-ready
solid body inside FreeCAD. It automatically accounts for central obstruction.
"""

import os
import FreeCAD as App
import Part

# 1. Telescope Specifications (Sky-Watcher SkyMax 127T)
D = 127.0       # Clear aperture diameter (mm)
F = 1500.0      # Focal length (mm)
D_obs = 45.0    # Central obstruction diameter (secondary mirror frame + tolerance)
thickness = 3.0 # Mask plate thickness (mm)

# 2. Parametric Calculations based on Bahtinov Formula
pitch = round(F / 170.0, 1)  # Resolves to ~8.8 mm for optimal diffraction
slot_w = pitch / 2.0         # Resolves to ~4.4 mm slot width

print(f"Initializing Bahtinov Mask compilation for Aperture={D}mm, Focus={F}mm...")
print(f"Calculated optimal values: Grating Pitch = {pitch}mm, Slot Width = {slot_w}mm")

# Initialize FreeCAD Document
doc = App.newDocument("Bahtinov_Mask_Project")

# 3. Base Plate Construction (Outer Mounting Rim)
outer_rim_d = D + 10.0  # Adding 10mm shoulder for mechanical alignment / friction fit
base_cylinder = Part.makeCylinder(outer_rim_d / 2.0, thickness)
aperture_cylinder = Part.makeCylinder(D / 2.0, thickness)

# Generate structural outer ring
mask_body = base_cylinder.cut(aperture_cylinder)

# Fuse structural solid central core under the secondary mirror obstruction area
central_disk = Part.makeCylinder(D_obs / 2.0, thickness)
mask_body = mask_body.fuse(central_disk)


# 4. Procedural Grating Generator Function
def make_grating(angle_deg, side_sign=0):
    """
    Generates an array of linear slots clipped to the telescope's aperture mask.
    
    Parameters:
        angle_deg (float): Rotation angle of slots (0 for vertical, +/-20 for angled)
        side_sign (int): Domain limiter. 0 = global, 1 = right hemisphere, -1 = left hemisphere
    """
    grating_shapes = []
    max_slots = int(D / pitch) + 2
    
    for i in range(-max_slots, max_slots):
        x_pos = i * pitch
        # Create single oversized structural block
        slot = Part.makeBox(slot_w, D + 20, thickness)
        # Center the block on local coordinates
        slot.translate(App.Vector(-slot_w / 2.0, -(D + 20) / 2.0, 0))
        # Step transform on X axis
        slot.translate(App.Vector(x_pos, 0, 0))
        # Rotate around global Z axis at target degree
        slot.rotate(App.Vector(0, 0, 0), App.Vector(0, 0, 1), angle_deg)
        grating_shapes.append(slot)
        
    # Compound array of all linear slots
    all_slots = Part.makeCompound(grating_shapes)
    
    # Define circular cutting boundaries
    cutter = Part.makeCylinder(D / 2.0, thickness)
    
    # If hemisphere mapping is requested (top split-grating)
    if side_sign != 0:
        half_box = Part.makeBox(D, D, thickness)
        if side_sign == -1:  # Limit to Left Side
            half_box.translate(App.Vector(-D, -D / 2.0, 0))
        else:  # Limit to Right Side
            half_box.translate(App.Vector(0, -D / 2.0, 0))
        cutter = cutter.common(half_box)
        
    return all_slots.common(cutter)


# 5. Constructing Multi-Zone Diffraction Arrays
# Bottom Half: Constant Vertical Slots (0 degrees)
lower_cutter = Part.makeBox(D + 20, D + 20, thickness)
lower_cutter.translate(App.Vector(-(D + 20) / 2.0, -(D + 20), 0))
vertical_zone = make_grating(0).common(lower_cutter)

# Top Half: Dynamic Split Angles (-20 and +20 degrees)
upper_cutter = Part.makeBox(D + 20, D + 20, thickness)
upper_cutter.translate(App.Vector(-(D + 20) / 2.0, 0, 0))

left_zone = make_grating(-20, side_sign=-1).common(upper_cutter)
right_zone = make_grating(20, side_sign=1).common(upper_cutter)

# Boolean operation: Assemble full slots matrix
all_mask_slots = vertical_zone.fuse(left_zone).fuse(right_zone)

# Clear the central obstruction core area to prevent floating artifacts inside slots
final_slots = all_mask_slots.cut(Part.makeCylinder(D_obs / 2.0 + 1, thickness))

# Subtract slot voids from the solid frame body (Mask Frame + Mask Inner Circle minus Slot Matrix)
bahtinov_mask = mask_body.fuse(Part.makeCylinder(D / 2.0, thickness).cut(final_slots))

# Register finalized parametric object into FreeCAD GUI Graph
mask_obj = doc.addObject("Part::Feature", "Bahtinov_SkyMax127")
mask_obj.Shape = bahtinov_mask
doc.recompute()

print("CAD solid body successfully generated inside FreeCAD environment.")

# 6. Automatic Industry-Standard File Export Pipeline
home_dir = os.path.expanduser("~")
stl_path = os.path.join(home_dir, "Bahtinov_SkyMax127.stl")
step_path = os.path.join(home_dir, "Bahtinov_SkyMax127.step")

try:
    Part.export([mask_obj], stl_path)
    Part.export([mask_obj], step_path)
    print(f"Pipeline Success! Files automatically deployed to your User Home directory:\n1. {stl_path}\n2. {step_path}")
except Exception as e:
    print(f"Export execution failed. Error logging: {str(e)}")
