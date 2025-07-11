import pandas as pd
import numpy as np
from ExtractSetups import extract_setups

def identify_unique_setups(LSD_CD_results, LSD_CL_results, LSD_CLF_results, LSD_CLR_results):
    # Step 1: Extract setup lists
    setupList_CD, setupList_CL, setupList_CLF, setupList_CLR = extract_setups(LSD_CD_results, LSD_CL_results, LSD_CLF_results, LSD_CLR_results)

    # Step 2: Combine all setups
    setupList = setupList_CD + setupList_CL + setupList_CLF + setupList_CLR

    # Step 3: Convert each setup to a string for uniqueness
    str_setup_list = [','.join(map(str, setup)) for setup in setupList]
    _, unique_indices = np.unique(str_setup_list, return_index=True)
    setupList_Unique = [setupList[i] for i in sorted(unique_indices)]

    # Step 4: Create DataFrame with one column of setup tuples
    UniqueSetups = pd.DataFrame({'[FRH, RRH, BG, FHS, RHS]': setupList_Unique})

    # Step 5: Initialize flags and indices
    num_unique = len(UniqueSetups)
    UniqueSetups['isInCD'] = False
    UniqueSetups['CDSetupIndex'] = np.nan
    UniqueSetups['isInCL'] = False
    UniqueSetups['CLSetupIndex'] = np.nan
    UniqueSetups['isInCLF'] = False
    UniqueSetups['CLFSetupIndex'] = np.nan
    UniqueSetups['isInCLR'] = False
    UniqueSetups['CLRSetupIndex'] = np.nan

    # Step 6: Populate flags and indices
    for i, setup in enumerate(UniqueSetups['[FRH, RRH, BG, FHS, RHS]']):
        if setup in setupList_CD:
            idx = setupList_CD.index(setup)
            UniqueSetups.at[i, 'isInCD'] = True
            UniqueSetups.at[i, 'CDSetupIndex'] = idx
        if setup in setupList_CL:
            idx = setupList_CL.index(setup)
            UniqueSetups.at[i, 'isInCL'] = True
            UniqueSetups.at[i, 'CLSetupIndex'] = idx
        if setup in setupList_CLF:
            idx = setupList_CLF.index(setup)
            UniqueSetups.at[i, 'isInCLF'] = True
            UniqueSetups.at[i, 'CLFSetupIndex'] = idx
        if setup in setupList_CLR:
            idx = setupList_CLR.index(setup)
            UniqueSetups.at[i, 'isInCLR'] = True
            UniqueSetups.at[i, 'CLRSetupIndex'] = idx

    return UniqueSetups
