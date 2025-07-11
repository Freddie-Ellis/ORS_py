import pandas as pd
import numpy as np

def append_corner_data(corner_info, data_table, settings):
    num_hs = 0
    num_ms = 0
    num_ls = 0

    # Determine phase angle
    if settings["UseCosPsi"] == 1:
        data_table["Phase"] = data_table["cospsi"]
    else:
        data_table["Phase"] = data_table["cosphi"]

    data_table = data_table.copy()
    data_table.insert(0, "Index", range(len(data_table)))
    data_table["Corner"] = 0
    data_table["CornerType"] = 0
    data_table["CornerType_Aero"] = 0
    data_table["Vsplit_LS"] = 0
    data_table["Vsplit_HS"] = 0

    for corner_number in range(corner_info.shape[1]):
        if corner_info[1, corner_number] > 0:
            start = corner_info[0, corner_number]
            length = corner_info[1, corner_number]
            end = start + length

            gating = (data_table["GLS"]) & (data_table["sLap"] >= start) & (data_table["sLap"] < end)
            cnr_data_temp = data_table[gating].copy()

            if "NCornerType_PHX" not in cnr_data_temp.columns and corner_info.shape[0] == 3 and not settings["CalculateCornerTypes"]:
                cnr_data_temp["NCornerType_PHX"] = corner_info[2, corner_number]

            cnr_data_temp["Corner"] = corner_number + 1

            if not cnr_data_temp.empty:
                phase = cnr_data_temp["Phase"].values
                phase_keep = np.ones(len(phase), dtype=bool)

                phase_min = phase.min()
                phase_min_ind = phase.argmin()
                if phase_min_ind > 0:
                    pre_min = phase[:phase_min_ind + 1]
                    threshold = phase_min + settings["PhaseMinMaxMargin"]
                    phase_keep[:phase_min_ind + 1] = pre_min <= threshold
                    phase[~phase_keep[:phase_min_ind + 1]] = phase_min

                phase_max = phase.max()
                phase_max_ind = phase.argmax()
                if phase_max_ind < len(phase) - 1:
                    post_max = phase[phase_max_ind:]
                    threshold = phase_max - settings["PhaseMinMaxMargin"]
                    phase_keep[phase_max_ind:] = post_max >= threshold

                cnr_data_temp = cnr_data_temp[phase_keep]

                if not cnr_data_temp.empty:
                    v_min = cnr_data_temp["vCar"].min()
                    cnr_data_temp["Vsplit_LS"] = cnr_data_temp["vCar"] <= settings["Vsplit_LSHS"]
                    cnr_data_temp["Vsplit_HS"] = cnr_data_temp["vCar"] > settings["Vsplit_LSHS"]

                    data_table.loc[cnr_data_temp["Index"], "Vsplit_LS"] = cnr_data_temp["Vsplit_LS"]
                    data_table.loc[cnr_data_temp["Index"], "Vsplit_HS"] = cnr_data_temp["Vsplit_HS"]

                    if ((cnr_data_temp["vCar"].iloc[0] - v_min > 1) and
                        (cnr_data_temp["vCar"].iloc[-1] - v_min > 1)) or \
                            cnr_data_temp["NCornerType_PHX"].mean() > 2.5:

                        if cnr_data_temp["cospsi"].iloc[0] < 0 and cnr_data_temp["cospsi"].iloc[-1] > 0:
                            aero_corners = np.zeros(len(cnr_data_temp), dtype=int)
                            v_car = cnr_data_temp["vCar"]

                            aero_corners[v_car <= settings["VmaxSplits_Aero"][0]] = 1
                            if len(settings["VmaxSplits_Aero"]) == 2:
                                aero_corners[(v_car > settings["VmaxSplits_Aero"][0]) & 
                                             (v_car <= settings["VmaxSplits_Aero"][1])] = 3
                            elif len(settings["VmaxSplits_Aero"]) == 3:
                                aero_corners[(v_car > settings["VmaxSplits_Aero"][0]) & 
                                             (v_car <= settings["VmaxSplits_Aero"][1])] = 2
                                aero_corners[(v_car > settings["VmaxSplits_Aero"][1]) & 
                                             (v_car <= settings["VmaxSplits_Aero"][2])] = 3

                            cnr_data_temp["CornerType_Aero"] = aero_corners

                            if settings["CalculateCornerTypes"]:
                                if len(settings["VmaxSplits"]) == 2:
                                    if v_min < settings["VmaxSplits"][0]:
                                        num_ls += 1
                                        cnr_data_temp["CornerType"] = 1
                                    elif v_min < settings["VmaxSplits"][1]:
                                        num_hs += 1
                                        cnr_data_temp["CornerType"] = 3
                                elif len(settings["VmaxSplits"]) == 3:
                                    if v_min < settings["VmaxSplits"][0]:
                                        num_ls += 1
                                        cnr_data_temp["CornerType"] = 1
                                    elif v_min < settings["VmaxSplits"][1]:
                                        num_ms += 1
                                        cnr_data_temp["CornerType"] = 2
                                    elif v_min < settings["VmaxSplits"][2]:
                                        num_hs += 1
                                        cnr_data_temp["CornerType"] = 3
                            else:
                                mean_type = cnr_data_temp["NCornerType_PHX"].mean()
                                if mean_type < 1.5:
                                    num_ls += 1
                                    cnr_data_temp["CornerType"] = 1
                                elif mean_type < 2.5:
                                    num_ms += 1
                                    cnr_data_temp["CornerType"] = 2
                                else:
                                    num_hs += 1
                                    cnr_data_temp["CornerType"] = 3

                            rows = cnr_data_temp["Index"]
                            data_table.loc[rows, "Corner"] = cnr_data_temp["Corner"]
                            data_table.loc[rows, "CornerType"] = cnr_data_temp["CornerType"]
                            data_table.loc[rows, "CornerType_Aero"] = cnr_data_temp["CornerType_Aero"]

    num_corners = pd.DataFrame({
        "NumLS": [num_ls],
        "NumMS": [num_ms],
        "NumHS": [num_hs]
    })

    return data_table, num_corners

