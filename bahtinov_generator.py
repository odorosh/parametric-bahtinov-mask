import sys
import os
import math
import FreeCAD as App
import Part

# 1. Telescope parameters (Sky-Watcher SkyMax 127T)
D = 127.0       # Clear aperture diameter (mm)
F = 1500.0      # Focal length (mm)
D_obs = 45.0    # Central obstruction diameter (mm)
thickness = 3.0 # Mask thickness (mm)
bridge_w = 6.0  # Horizontal structural bridge width (mm)

# 2. Bahtinov grating calculations
pitch = round(F / 170.0, 1)  # Grid pitch ~8.8 mm
slot_w = pitch / 2.0         # Slot width ~4.4 mm

# Create new FreeCAD document
doc = App.newDocument("Bahtinov_Mask_Project")

# 3. Base outer rim configuration
outer_rim_d = D + 10.0
base_cylinder = Part.makeCylinder(outer_rim_d / 2.0, thickness)
aperture_cylinder = Part.makeCylinder(D / 2.0, thickness)
mask_body = base_cylinder.cut(aperture_cylinder)

# Central obstruction blank disk
central_disk = Part.makeCylinder(D_obs / 2.0, thickness)
mask_body = mask_body.fuse(central_disk)

# Horizontal structural bridge
horizontal_bridge = Part.makeBox(D + 20.0, bridge_w, thickness)
horizontal_bridge.translate(App.Vector(-(D + 20.0) / 2.0, -bridge_w / 2.0, 0))
horizontal_bridge = horizontal_bridge.common(Part.makeCylinder(D / 2.0, thickness))
mask_body = mask_body.fuse(horizontal_bridge)

# 4. Functional definition for parametric grating generation
def make_grating(angle_deg, side_sign=0):
    grating_shapes = []
    max_slots = int(D / pitch) + 2

    for i in range(-max_slots, max_slots):
        x_pos = i * pitch
        slot = Part.makeBox(slot_w, D + 20, thickness)
        slot.translate(App.Vector(-slot_w / 2.0, -(D + 20) / 2.0, 0))
        slot.translate(App.Vector(x_pos, 0, 0))
        slot.rotate(App.Vector(0,0,0), App.Vector(0,0,1), angle_deg)
        grating_shapes.append(slot)

    all_slots = Part.makeCompound(grating_shapes)
    cutter = Part.makeCylinder(D / 2.0, thickness)

    if side_sign != 0:
        half_box = Part.makeBox(D, D, thickness)
        if side_sign == -1:
            half_box.translate(App.Vector(-D, -D/2.0, 0))
        else:
            half_box.translate(App.Vector(0, -D/2.0, 0))
        cutter = cutter.common(half_box)

    return all_slots.common(cutter)

# 5. Generate and isolate individual diffraction zones
# Спочатку створюємо абсолютно суцільну заготовку
# (Основа + глухий центр + місток) як один моноліт
blank_solid = mask_body

# Тепер генеруємо щілини (решітку)
lower_cutter = Part.makeBox(D + 20, D + 20, thickness)
lower_cutter.translate(App.Vector(-(D + 20)/2.0, -(D + 20), 0))
vertical_zone = make_grating(0).common(lower_cutter)

upper_cutter = Part.makeBox(D + 20, D + 20, thickness)
upper_cutter.translate(App.Vector(-(D + 20)/2.0, 0, 0))

left_zone = make_grating(-20, side_sign=-1).common(upper_cutter)
right_zone = make_grating(20, side_sign=1).common(upper_cutter)

# Об'єднуємо всі щілини в один загальний різальний інструмент (Compound)
all_slots = vertical_zone.fuse(left_zone).fuse(right_zone)

# Готуємо зони, які НЕ МОЖНА різати (захист центру і містка)
central_protection = Part.makeCylinder(D_obs / 2.0, thickness)
bridge_protection = Part.makeBox(D + 20.0, bridge_w, thickness)
bridge_protection.translate(App.Vector(-(D + 20.0) / 2.0, -bridge_w / 2.0, 0))

# Очищуємо інструмент різання: прибираємо щілини з містка та центру
final_cutting_tool = all_slots.cut(central_protection).cut(bridge_protection)

# ОДНА ОПЕРАЦІЯ ВИРІЗАННЯ: віднімаємо щілини від суцільного диска апертури
aperture_disk = Part.makeCylinder(D / 2.0, thickness)
slotted_aperture = aperture_disk.cut(final_cutting_tool)

# З'єднуємо апертуру із зовнішнім посадковим кільцем
bahtinov_mask = blank_solid.fuse(slotted_aperture)

# Застосовуємо фінальне згладжування швів
clean_bahtinov_mask = bahtinov_mask.removeSplitter()

# Реєструємо фінальний об'єкт у дереві FreeCAD
mask_obj = doc.addObject("Part::Feature", "Bahtinov_SkyMax127_Perfect")
mask_obj.Shape = clean_bahtinov_mask
doc.recompute()

print("Проєкт повністю оптимізовано! Модель ідеально чиста.")
# =========================================================

# =========================================================
# 6. НАДІЙНИЙ ЕКСПОРТ У ВАШУ РОБОЧУ ПАПКУ
# =========================================================
# ВСТАВТЕ СЮДИ ВАШ ТОЧНИЙ ШЛЯХ, ЯКИЙ ПОКАЗАЛА КОМАНДА `pwd`
target_dir = "/home/user/projects/bahtinov"

# Формуємо точні шляхи до інженерних файлів
stl_path = os.path.join(target_dir, "Bahtinov_SkyMax127.stl")
step_path = os.path.join(target_dir, "Bahtinov_SkyMax127.step")
fcstd_path = os.path.join(target_dir, "Bahtinov_SkyMax127.FCStd")

# Експортуємо інженерні формати
Part.export([mask_obj], stl_path)
Part.export([mask_obj], step_path)

# Додатково автоматично зберігаємо рідний файл FreeCAD для ручного редагування
doc.saveAs(fcstd_path)

print(f"\n[УСПІХ] Усі файли записано безпосередньо у вашу папку:")
print(f"1. STL (для 3D-друку): {stl_path}")
print(f"2. STEP (для CAD/редагування): {step_path}")
print(f"3. FCStd (проєкт FreeCAD): {fcstd_path}")
# =========================================================
