import pandas as pd
import numpy as np

def generate_apex_delta(all_sessions_data: pd.DataFrame) -> pd.DataFrame:
    # Define excluded channel names
    excluded_chan_names = {
        'SessionIndex', 'BGripLimited', 'NCornerType_PHX', 'BNRearWingStateControlMode',
        'cospsi', 'cosphi', 'GLS', 'PLS', 'Phase', 'Index', 'Corner', 'CornerType',
        'Vsplit_LS', 'Vsplit_HS'
    }

    # Determine which channels to average
    chan_names = list(all_sessions_data.columns)
    avg_apex_chan_names = [ch for ch in chan_names if ch not in excluded_chan_names]

    # Extract unique corner indices, excluding 0
    corner_indices = all_sessions_data['Corner'].unique()
    corner_indices = corner_indices[corner_indices != 0]

    # Initialize dictionary to collect apex delta data
    apex_delta_data = {}

    for chan_name in chan_names:
        if chan_name not in avg_apex_chan_names:
            apex_delta_data[chan_name] = all_sessions_data[chan_name]
        else:
            chan_col = all_sessions_data[chan_name].copy()
            for corner in corner_indices:
                # Identify rows within the cosine window for the current corner
                mask = (
                    (all_sessions_data['Corner'] == corner) &
                    (all_sessions_data['cospsi'] >= -0.2) &
                    (all_sessions_data['cospsi'] <= 0.2)
                )
                if mask.any():
                    avg_apex = chan_col[mask].mean()
                    chan_col[mask] = chan_col[mask] - avg_apex
            apex_delta_data[chan_name] = chan_col

    # Convert the dictionary to a DataFrame
    apex_delta_df = pd.DataFrame(apex_delta_data)
    return apex_delta_df

