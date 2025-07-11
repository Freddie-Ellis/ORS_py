import pandas as pd
import numpy as np
from IdentifyUniqueSetups import identify_unique_setups
from AppendCornerData import append_corner_data
from LoadSensData import load_sens_data
from LoadChanData import load_chan_data
from GetDLSSetupInfo import get_dls_setup_info
from pythonwrapper import Pep
import scipy.io


# Main function
def ImportDLSData(LSD_CD_results, LSD_CL_results, LSD_CLF_results, LSD_CLR_results, TrackName, numSetups, Settings):
    services = Pep.get_services()
    carSetupService = services.car_setup_service

    AllCornerInfo = scipy.io.loadmat('CornerData_2022Tracks.mat')

    UniqueSetups = identify_unique_setups(LSD_CD_results, LSD_CL_results, LSD_CLF_results, LSD_CLR_results)
    numUniqueSetups = len(UniqueSetups)

    SetupInfo = pd.DataFrame()
    DLSData = pd.DataFrame()
    NumCorners = pd.DataFrame()

    for nSetup in range(numUniqueSetups):
        isSensInSetup = UniqueSetups.iloc[nSetup]
        nSetupIdx = numSetups + nSetup

        if isSensInSetup['isInCD']:
            idx = isSensInSetup['CDSetupIndex']
            TempSetupInfo = get_dls_setup_info(LSD_CD_results, idx)
            TempDLSData = pd.DataFrame(LSD_CD_results[idx]['DLS_BSL'])
            TempDLSData = load_chan_data(TempDLSData, Settings)

        elif isSensInSetup['isInCL']:
            idx = isSensInSetup['CLSetupIndex']
            TempSetupInfo = get_dls_setup_info(LSD_CL_results, idx)
            TempDLSData = pd.DataFrame(LSD_CL_results[idx]['DLS_BSL'])
            TempDLSData = load_chan_data(TempDLSData, Settings)

        elif isSensInSetup['isInCLF']:
            idx = isSensInSetup['CLFSetupIndex']
            TempSetupInfo = get_dls_setup_info(LSD_CLF_results, idx)
            TempDLSData = pd.DataFrame(LSD_CLF_results[idx]['DLS_BSL'])
            TempDLSData = load_chan_data(TempDLSData, Settings)

        elif isSensInSetup['isInCLR']:
            idx = isSensInSetup['CLRSetupIndex']
            TempSetupInfo = get_dls_setup_info(LSD_CLR_results, idx)
            TempDLSData = pd.DataFrame(LSD_CLR_results[idx]['DLS_BSL'])
            TempDLSData = load_chan_data(TempDLSData, Settings)

        TempDLSData = load_sens_data(isSensInSetup, TempDLSData, LSD_CD_results, LSD_CL_results, LSD_CLF_results, LSD_CLR_results)

        TempDLSData['GLS'] = TempDLSData.get('rThrottle', pd.Series([100]*len(TempDLSData))) < 98
        TempDLSData['PLS'] = TempDLSData.get('rThrottle', pd.Series([100]*len(TempDLSData))) >= 98

        carSetup = carSetupService.GetCarSetup(TempSetupInfo['setup_ID'][0])
        SessionType = Settings.get('DLSSessionType', 'DLS_Qu')
        TempCarSetupInfo = pd.DataFrame({
            'SetupIndex': [nSetupIdx],
            'Track': [TrackName],
            'SessionType': [SessionType],
            'EventCode': [carSetup.EventCode]
        })
        TempSetupInfo = pd.concat([TempCarSetupInfo, TempSetupInfo, pd.DataFrame([isSensInSetup])], axis=1)

        CornerStart = carSetup.GetParameterValue("sCornerStartDistance")
        CornerEnd = carSetup.GetParameterValue("sCornerEndDistance")
        CornerLength = CornerEnd - CornerStart
        CornerSpeed = carSetup.GetParameterValue("nCornerSpeed")
        CornerInfo = np.array([CornerStart, CornerLength, CornerSpeed])

        if np.isnan(CornerInfo).any():
            CornerInfo = AllCornerInfo[TrackName].T
            CornerInfo[1] = CornerInfo[1] - CornerInfo[0]

        TempDLSData, TempNumCorners = append_corner_data(CornerInfo, TempDLSData, Settings)

        TempDLSData.insert(0, 'SetupIndex', nSetupIdx)

        if nSetup > 0:
            SetupInfo = pd.concat([SetupInfo, TempSetupInfo], ignore_index=True)
            DLSData = pd.concat([DLSData, TempDLSData], ignore_index=True)
            NumCorners = pd.concat([NumCorners, TempNumCorners], ignore_index=True)
        else:
            SetupInfo = TempSetupInfo
            DLSData = TempDLSData
            NumCorners = TempNumCorners

    return SetupInfo, DLSData, NumCorners

