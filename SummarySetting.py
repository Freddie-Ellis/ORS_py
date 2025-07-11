Settings = {
    "LoadTrackData": 0,
    "TrackData": 0,
    "LoadVoyagerData": 0,
    "VoyagerData": 0,
    "VoyagerSessionType": "Voyager_Qu",
    "LoadDLSData": 1,
    "DLSData": 1,
    "DLSSessionType": "DLS_Qu",
    "DataChoice": 3,  # 1=Raw, 2=Filtered, 3=FilteredGLS
    "SavePDF": 0,
    "SplitBySession": 0,
    "CornerPhaseOrder": 0,
    "FCamber_WT": -999,
    "RCamber_WT": -999,
    "FToe_WT": 0,
    "RToe_WT": 0,
    "AB_Tgt_WT": 47,
    "RRH_Static_WT": 999,
    "PercInd": [5, 95],
    "StaticFRH_Ylim": [15, 50],
    "StaticRRH_Ylim": [30, 100],
    "StaticCamberF_Ylim": [-4, -1],
    "StaticCamberR_Ylim": [-2, -0.5],
    "StaticToeF_Ylim": [-5, 1],
    "StaticToeR_Ylim": [-3, 3],
    "FWFlap_Ylim": [0, 20],
    "CatAB_Ylim": [40, 50],
    "CatCd_Ylim": [0.9, 1.3],
    "CatCl_Ylim": [-4.8, -3.5],
    "AB150_Ylim": [0, 100],
    "Cd225_Ylim": [0, 2],
    "Cl150_Ylim": [-6, -3],
    "VmaxSplits": [115, 175, 300],
    "VmaxSplits_Aero": [160, 250],
    "Vmax_Low": 115,
    "Vmax_Medium": 175,
    "Vmax_High": 300,
    "CalculateCornerTypes": 0,
    "Vsplit_LSHS": 200,
    "CosPhiBounds": [-1, -0.95, -0.6, -0.2, 0.2, 0.45, 0.7, 1],
    "UseCosPsi": 1,
    "CosPsi_gLong_Offset": -0.2,
    "CosPsi_gLong_Offset_Coeffs": [-3.013688567, 0.043917649, -0.001566442],
    "PLSpeeds": list(range(150, 351, 25)),
    "PhaseMinMaxMargin": 0.03,
    "ClfLoc": 0,
    "ClrLoc": 600,
    "FWLoc": -800,
    "FACLLoc": 0,
    "CofGLoc": 1900,
    "RACLLoc": 3700,
    "FiltFreq": 5
}

# Conditional assignment for DrvCodes
Settings["DrvCodes"] = [["VOY"], ["VOY"]] if Settings["VoyagerData"] else [["GAS"], ["OCO"]]
