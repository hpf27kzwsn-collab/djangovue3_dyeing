"""包装净重计算；未测量与明确零值分别处理。"""


def weighed_net_mass_kg(gross_mass_kg, tube_unit_tare_kg, piece_quantity, outer_tare_kg):
    if any(value is None for value in (gross_mass_kg, tube_unit_tare_kg, piece_quantity, outer_tare_kg)):
        return None
    return gross_mass_kg - tube_unit_tare_kg * piece_quantity - outer_tare_kg


def fixed_net_mass_kg(fixed_piece_mass_kg, piece_quantity):
    if fixed_piece_mass_kg is None or piece_quantity is None:
        return None
    return fixed_piece_mass_kg * piece_quantity
