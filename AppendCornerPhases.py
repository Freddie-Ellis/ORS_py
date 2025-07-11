import pandas as pd
from GenerateApexDelta import generate_apex_delta
from GetPhaseData import get_phase_data

def AppendCornerPhases(Settings, SetupInfo, Data):
    # Apply apex deltas to all corners
    ApexDeltaData = generate_apex_delta(Data)

    # Generate curve-fits for loaded radius and vertical load as functions of ride-heights and roll angle
    ChanNames = Data.columns

    if 'hRideRCalc' not in ChanNames:
        Data['OffsetRRH'] = Data['hRideRLaser']
        Data['OffsetFRH'] = Data['hRideFLaser']
    else:
        Data['OffsetRRH'] = Data['hRideRCalc']
        Data['OffsetFRH'] = Data['hRideFCalc']

    AvgSetupRRH = SetupInfo['RRH'].mean()
    AvgSetupFRH = SetupInfo['FRH'].mean()

    numSetups = len(SetupInfo)

    # Offset RHs to account for differences in static setting between laps
    for nSetup in range(1, numSetups + 1):
        RRHAdjustment = AvgSetupRRH - SetupInfo.loc[nSetup - 1, 'RRH']
        FRHAdjustment = AvgSetupFRH - SetupInfo.loc[nSetup - 1, 'FRH']

        LapInd = Data['SetupIndex'] == nSetup
        Data.loc[LapInd, 'OffsetRRH'] += RRHAdjustment
        Data.loc[LapInd, 'OffsetFRH'] += FRHAdjustment

    # Split data by corner phases
    Data = get_phase_data(Settings, Data)
    ApexDeltaData = get_phase_data(Settings, ApexDeltaData)

    return Data, ApexDeltaData

