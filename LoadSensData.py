import pandas as pd
import numpy as np

def load_sens_data(sens_setup_info, temp_chan_data, lsd_cd_results, lsd_cl_results, lsd_clf_results, lsd_clr_results):
    # Initialize an empty DataFrame with NaNs
    temp_sens_data = pd.DataFrame(np.nan, index=range(len(temp_chan_data)), columns=[
        'CD_int', 'LSD_CD', 'CL_int', 'LSD_CL', 'CLF_int', 'LSD_CLF', 'CLR_int', 'LSD_CLR'
    ])

    # Helper function to convert MATLAB struct to DataFrame
    def struct_to_dataframe(mat_struct):
        return pd.DataFrame({k: v.T if hasattr(v, 'T') else v for k, v in mat_struct.items()})

    # CD sensitivities
    if sens_setup_info['isInCD']:
        idx_cd = sens_setup_info['CDSetupIndex']
        cd_sens_data = struct_to_dataframe(lsd_cd_results[idx_cd]['DLS_sens'][0, 0])
        temp_sens_data[['CD_int', 'LSD_CD']] = cd_sens_data[['CD_int', 'LSD_CD']]

    # CL sensitivities
    if sens_setup_info['isInCL']:
        idx_cl = sens_setup_info['CLSetupIndex']
        cl_sens_data = struct_to_dataframe(lsd_cl_results[idx_cl]['DLS_sens'][0, 0])
        temp_sens_data[['CL_int', 'LSD_CL']] = cl_sens_data[['CL_int', 'LSD_CL']]

    # CLF sensitivities
    if sens_setup_info['isInCLF']:
        idx_clf = sens_setup_info['CLFSetupIndex']
        clf_sens_data = struct_to_dataframe(lsd_clf_results[idx_clf]['DLS_sens'][0, 0])
        temp_sens_data[['CLF_int', 'LSD_CLF']] = clf_sens_data[['CLF_int', 'LSD_CLF']]

    # CLR sensitivities
    if sens_setup_info['isInCLR']:
        idx_clr = sens_setup_info['CLRSetupIndex']
        clr_sens_data = struct_to_dataframe(lsd_clr_results[idx_clr]['DLS_sens'][0, 0])
        temp_sens_data[['CLR_int', 'LSD_CLR']] = clr_sens_data[['CLR_int', 'LSD_CLR']]

    # Append sensitivity data to the main channel data
    temp_chan_data = pd.concat([temp_chan_data.reset_index(drop=True), temp_sens_data], axis=1)

    return temp_chan_data

