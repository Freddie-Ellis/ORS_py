import pandas as pd
import numpy as np

def get_phase_data(settings, data):
    cos_phi_bounds = settings["CosPhiBounds"]
    use_cospsi = settings["UseCosPsi"]
    ggv_angle = "cospsi" if use_cospsi == 1 else "cosphi"

    # Ensure the angle column exists
    if ggv_angle not in data.columns:
        raise ValueError(f"Required column '{ggv_angle}' not found in data.")

    # Identify unique corners excluding 0
    corners = data["Corner"].unique()
    corners = corners[corners != 0]

    # Initialize CornerPhase column
    corner_phase_col = np.zeros(len(data), dtype=int)

    # Assign corner phases based on angle bounds
    for n_corner in corners:
        for c_phase in range(len(cos_phi_bounds) - 1):
            mask = (
                (data["Corner"] == n_corner) &
                (data[ggv_angle] >= cos_phi_bounds[c_phase]) &
                (data[ggv_angle] < cos_phi_bounds[c_phase + 1])
            )
            corner_phase_col[mask] = c_phase + 1  # MATLAB is 1-indexed

    data["CornerPhase"] = corner_phase_col

    # Identify low-speed braking zone
    ls_brk_ind = (
        data["Vsplit_LS"] &
        (data[ggv_angle] >= cos_phi_bounds[0]) &
        (data[ggv_angle] < cos_phi_bounds[1])
    )
    data["LSBrk"] = ls_brk_ind

    # Identify high-speed braking zone
    hs_brk_ind = (
        data["Vsplit_HS"] &
        (data[ggv_angle] >= cos_phi_bounds[0]) &
        (data[ggv_angle] < cos_phi_bounds[1])
    )
    data["HSBrk"] = hs_brk_ind

    return data

