import pandas as pd

def get_dls_setup_info(dls_data, idx):
    # Extract the all_info struct from the specified index
    dls_all_info = dls_data[idx]['all_info']

    # Initialize a dictionary to hold setup information
    setup_info = {
        'setup_ID': dls_all_info['setup_ID'][0],
        'setup_name': dls_all_info['setup_name'][0],
        'FRH': float(dls_all_info['hRideSetupF'][0]) * 1000,  # Convert from meters to mm
        'RRH': float(dls_all_info['hRideStaticR'][0]) * 1000,  # Convert from meters to mm
        'xBumpGapSetupFM': dls_all_info['xBumpGapSetupFM'][0],
        'rMechBalOffset': dls_all_info['rMechBalOffset'][0],
        'CAeroBalOffset': dls_all_info['CAeroBalOffset'][0],
        'successRebal': dls_all_info['successRebal'][0],
        'hRideSetupF_Offset': dls_all_info['hRideSetupF_Offset'][0],
        'hRideStaticR_Offset': dls_all_info['hRideStaticR_Offset'][0],
        'DLL': dls_all_info['DLL'][0]
    }

    # Clean and add Component2_key and slice_key as column names
    key_fhs = dls_all_info['Component2_key'][0].replace(' ', '')
    val_fhs = dls_all_info['Component2_value'][0]
    setup_info[key_fhs] = val_fhs

    key_rhs = dls_all_info['slice_key'][0].replace(' ', '')
    val_rhs = str(dls_all_info['slice_value'][0])
    setup_info[key_rhs] = val_rhs

    # Convert the dictionary to a pandas DataFrame
    setup_info_df = pd.DataFrame([setup_info])

    return setup_info_df

