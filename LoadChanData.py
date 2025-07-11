import numpy as np
import pandas as pd

def load_chan_data(data_table: pd.DataFrame, settings: dict) -> pd.DataFrame:
    chan_names = data_table.columns.tolist()

    # Rename channels for Voyager data
    if settings.get("VoyagerData", False):
        if 'aWheelFRoadOuter' in chan_names:
            data_table = data_table.rename(columns={'aWheelFRoadOuter': 'aWheelFRoad'})
        if 'qFactor' in chan_names:
            data_table = data_table.rename(columns={'qFactor': 'QFactor'})

    # Rename curvature
    if settings.get("VoyagerData", False) or settings.get("DLSData", False):
        if 'rCurvature' in chan_names:
            data_table = data_table.rename(columns={'rCurvature': 'Curvature'})

    # Sign of front road wheels steered angle
    sgn_str = np.sign(data_table['aWheelFRoad'])
    sgn_str[sgn_str == 0] = 1

    # QFactor
    if 'TurbineQFactor' in chan_names:
        data_table['QFactor'] = data_table['TurbineQFactor']

    # Derived yaw channels
    if all(col in chan_names for col in ['aAeroYaw', 'nYaw', 'vCar']):
        vCar = data_table['vCar'].replace(0, np.nan)
        data_table['ClfYaw'] = (data_table['aAeroYaw'] - (36 / 1e4) * settings['ClfLoc'] * data_table['nYaw'] / vCar) * -sgn_str
        data_table['ClrYaw'] = (data_table['aAeroYaw'] - (36 / 1e4) * settings['ClrLoc'] * data_table['nYaw'] / vCar) * -sgn_str
        data_table['FWYaw'] = (data_table['aAeroYaw'] - (36 / 1e4) * settings['FWLoc'] * data_table['nYaw'] / vCar) * -sgn_str
        data_table['RACLYaw'] = (data_table['aAeroYaw'] - (36 / 1e4) * settings['RACLLoc'] * data_table['nYaw'] / vCar) * -sgn_str
        if not settings.get("VoyagerData", False):
            data_table['CofGYaw'] = (data_table['aAeroYaw'] - (36 / 1e4) * settings['CofGLoc'] * data_table['nYaw'] / vCar) * -sgn_str

    # Slip angles
    if 'aSlipCofG' in chan_names:
        if all(col in chan_names for col in ['nYaw', 'vCar']):
            vCar = data_table['vCar'].replace(0, np.nan)
            data_table['FACLSlip'] = (data_table['aSlipCofG'] - (36 / 1e4) * -1900 * data_table['nYaw'] / vCar) * -sgn_str
        data_table['CofGSlip'] = data_table['aSlipCofG'] * -sgn_str

    # Front and rear axle-average tyre slip angle
    if settings.get("VoyagerData", False):
        data_table['aSlipF'] = -np.abs(data_table[['aSlipFL', 'aSlipFR']].mean(axis=1))
        data_table['aSlipR'] = -np.abs(data_table[['aSlipRL', 'aSlipRR']].mean(axis=1))
    else:
        if 'aSlipF' in chan_names:
            data_table['aSlipF'] = -np.abs(data_table['aSlipF'])
        if 'aSlipR' in chan_names:
            data_table['aSlipR'] = -np.abs(data_table['aSlipR'])

    # Inner/outer channels
    def load_io_channels(sign, left, right):
        inner = np.where(sign > 0, left, right)
        outer = np.where(sign > 0, right, left)
        return inner, outer

    if all(col in chan_names for col in ['aCamberFL', 'aCamberFR', 'aCamberRL', 'aCamberRR']):
        data_table['aCamberFI'], data_table['aCamberFO'] = load_io_channels(sgn_str, data_table['aCamberFL'], data_table['aCamberFR'])
        data_table['aCamberRI'], data_table['aCamberRO'] = load_io_channels(sgn_str, data_table['aCamberRL'], data_table['aCamberRR'])

    if all(col in chan_names for col in ['FVerticalFL', 'FVerticalFR', 'FVerticalRL', 'FVerticalRR']):
        data_table['FVerticalFI'], data_table['FVerticalFO'] = load_io_channels(sgn_str, data_table['FVerticalFL'], data_table['FVerticalFR'])
        data_table['FVerticalRI'], data_table['FVerticalRO'] = load_io_channels(sgn_str, data_table['FVerticalRL'], data_table['FVerticalRR'])

    if all(col in chan_names for col in ['rTyreLoadedFL', 'rTyreLoadedFR', 'rTyreLoadedRL', 'rTyreLoadedRR']):
        data_table['rTyreLoadedFI'], data_table['rTyreLoadedFO'] = load_io_channels(sgn_str, data_table['rTyreLoadedFL'], data_table['rTyreLoadedFR'])
        data_table['rTyreLoadedRI'], data_table['rTyreLoadedRO'] = load_io_channels(sgn_str, data_table['rTyreLoadedRL'], data_table['rTyreLoadedRR'])

    if all(col in chan_names for col in ['FLateralFL', 'FLateralFR', 'FLateralRL', 'FLateralRR']):
        data_table['FLateralFI'], data_table['FLateralFO'] = load_io_channels(sgn_str, data_table['FLateralFL'], data_table['FLateralFR'])
        data_table['FLateralRI'], data_table['FLateralRO'] = load_io_channels(sgn_str, data_table['FLateralRL'], data_table['FLateralRR'])
        for col in ['FLateralFI', 'FLateralFO', 'FLateralRI', 'FLateralRO']:
            data_table[col] = np.abs(data_table[col])

    if all(col in chan_names for col in ['FLongFL', 'FLongFR', 'FLongRL', 'FLongRR']):
        data_table['FLongFI'], data_table['FLongFO'] = load_io_channels(sgn_str, data_table['FLongFL'], data_table['FLongFR'])
        data_table['FLongRI'], data_table['FLongRO'] = load_io_channels(sgn_str, data_table['FLongRL'], data_table['FLongRR'])

    # Update steer, roll and curvature
    data_table['aRoll'] = data_table['aRoll'] * -sgn_str
    data_table['aWheelFRoad'] = data_table['aWheelFRoad'] * sgn_str
    data_table['Curvature'] = data_table['Curvature'] * sgn_str

    # Update dynamic pressure
    if settings.get("VoyagerData", False):
        if 'pPitot' in chan_names:
            data_table['pDynamic_Global'] = data_table['pPitot'] * 100
    else:
        if 'pDynamic_Global' in chan_names:
            data_table['pDynamic_Global'] = data_table['pDynamic_Global'] * 100

    # Compute cosphi and cospsi for DLS data
    if settings.get("DLSData", False):
        data_table['cosphi'] = data_table['gLong'] / np.sqrt(data_table['gLong']**2 + data_table['gLat']**2)
        vCar_MS = data_table['vCar'] / 3.6
        gLong_offset = (np.vstack([np.ones_like(vCar_MS), vCar_MS, vCar_MS**2]).T @ np.array(settings['CosPsi_gLong_Offset_Coeffs'])) / 9.81
        gLong_with_offset = data_table['gLong'] - gLong_offset
        data_table['cospsi'] = data_table['cosphi']
        if settings.get("UseCosPsi", False):
            data_table['cosphi'] = gLong_with_offset / np.sqrt(gLong_with_offset**2 + data_table['gLat']**2)

    return data_table

