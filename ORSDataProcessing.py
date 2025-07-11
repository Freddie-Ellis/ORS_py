import os
import pandas as pd
import pyarrow.parquet as pq
import pyarrow as pa
from tkinter import Tk, filedialog
#from scipy.io import loadmat
from tqdm import tqdm
from scipy.io import loadmat
from AppendCornerPhases import AppendCornerPhases
from ImportDLSData import ImportDLSData
# Load settings
from SummarySetting import Settings # Assumes you have a Python file with the Settings dictionary

def read_csv_column_pairs(file_path, start_index=1):
    with open(file_path, 'r') as f:
        lines = f.read().split(',')
    indices = list(range(start_index, len(lines) - 1, 2))
    return [lines[i] for i in indices], [lines[i + 1] for i in indices]

def read_csv_column_pairs_from_index(file_path, start_index=3):
    with open(file_path, 'r') as f:
        lines = f.read().split(',')
    indices = list(range(start_index, len(lines) - 1, 2))
    return [lines[i] for i in indices], [lines[i + 1] for i in indices]

def save_parquet(df, path):
    table = pa.Table.from_pandas(df)
    pq.write_table(table, path)

def LoadDLSFilePaths(root_folder):

    DLSFileList = []

    for dirpath, _, filenames in os.walk(root_folder):

        #print(f"Checking directory: {dirpath}")
        #print(f"Checking file name: {filenames}")
        # Filter .mat files in the current directory
        mat_files = [f for f in filenames if f.endswith('.mat')]
        #print(mat_files)
        # Create a dictionary to map file types to their paths
        file_dict = {}
        for f in mat_files:
            lower_f = f.lower()
            full_path = os.path.join(dirpath, f)
            if 'cd' in lower_f:
                file_dict['CD'] = full_path
                #print("CD FOUND!")
            elif 'clf' in lower_f:
                file_dict['CLF'] = full_path
            elif 'clr' in lower_f:
                file_dict['CLR'] = full_path
            elif 'cl' in lower_f and 'clf' not in lower_f and 'clr' not in lower_f:
                file_dict['CL'] = full_path

        # If all four required files are found, add them in the correct order
        if all(k in file_dict for k in ['CD', 'CLF', 'CLR', 'CL']):
            DLSFileList.append([
                file_dict['CD'],
                file_dict['CLF'],
                file_dict['CLR'],
                file_dict['CL']
            ])

    return DLSFileList

def ImportTrackData(session_paths, session_filenames, tracks, setup_ids, settings):
    return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

def ImportVoyagerData(tracks, setup_ids, settings):
    return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

# Hide the root window
Tk().withdraw()

# Open folder selection dialog
rootDLSFolder = filedialog.askdirectory(title="Select folder containing ALL DLS data")

# Load DLS file paths
DLSFileList = LoadDLSFilePaths(rootDLSFolder)

# Load DLS Data
if Settings["LoadDLSData"] == 1:
    Settings["DLSData"] = 1

    numSetups = 0
    
    for nFolder, nFileList in enumerate(tqdm(DLSFileList, desc="Processing DLS folders")):
        filepath = os.path.dirname(nFileList[0])
        print("Full path:", filepath)

        # Go two levels up to get the track folder (e.g., "BAR_LSDs_Iss1_LSD_Processed")
        track_folder_path = os.path.dirname(filepath)
        track_folder = os.path.basename(track_folder_path)
        #print("Track folder:", track_folder)

        # Extract the track name (e.g., "BAR")
        TrackName = track_folder.split('_')[0]
        #print("Track name:", TrackName)
        
        LSD_CD_results = loadmat(nFileList[0])["LSD_results"]
        LSD_CLF_results = loadmat(nFileList[1])["LSD_results"]
        LSD_CLR_results = loadmat(nFileList[2])["LSD_results"]
        LSD_CL_results = loadmat(nFileList[3])["LSD_results"]
        #print(LSD_CD_results[0].shape)
        #print(LSD_CD_results[0].tolist())
        nDLSSetupInfo, nDLSData, nDLSNumCorners = ImportDLSData(LSD_CD_results, LSD_CL_results, LSD_CLF_results, LSD_CLR_results, TrackName, numSetups, Settings)
        nDLSData, nDLSApexDeltaData = AppendCornerPhases(Settings, nDLSSetupInfo, nDLSData)

        #print(f"Processed folder {nFolder + 1}: {TrackName}")
        #print(f"nDLSSetupInfo shape: {nDLSSetupInfo.shape}")

        if nFolder == 0:
            DLSSetupInfo, DLSData, DLSNumCorners, DLSApexDeltaData = (nDLSSetupInfo, nDLSData, nDLSNumCorners, nDLSApexDeltaData)
        else:
            DLSSetupInfo = pd.concat([DLSSetupInfo, nDLSSetupInfo])
            DLSData = pd.concat([DLSData, nDLSData])
            DLSNumCorners = pd.concat([DLSNumCorners, nDLSNumCorners])
            DLSApexDeltaData = pd.concat([DLSApexDeltaData, nDLSApexDeltaData])

        numSetups = len(DLSSetupInfo)

    save_parquet(DLSSetupInfo, "C:/tools/setup_DLS.parquet")
    save_parquet(DLSData, "C:/tools/data_DLS.parquet")
    save_parquet(DLSNumCorners, "C:/tools/corners_DLS.parquet")
    save_parquet(DLSApexDeltaData, "C:/tools/apexdelta_DLS.parquet")
    Settings["DLSData"] = 0

# Load Track Data
if Settings["LoadTrackData"] == 1:
    Settings["TrackData"] = 1
    ssn_file = input("Enter path to Track SSN CSV file: ")
    SessionPaths, SessionFilenames = read_csv_column_pairs(ssn_file, start_index=0)

    setup_file = input("Enter path to Track SetupIDs CSV file: ")
    Tracks, SetupIDs = read_csv_column_pairs_from_index(setup_file, start_index=3)

    TrackSetupInfo, TrackData, TrackNumCorners = ImportTrackData(SessionPaths, SessionFilenames, Tracks, SetupIDs, Settings)
    TrackData, TrackApexDeltaData = AppendCornerPhases(Settings, TrackSetupInfo, TrackData)

    save_parquet(TrackSetupInfo, "setup_Track.parquet")
    save_parquet(TrackData, "data_Track.parquet")
    save_parquet(TrackNumCorners, "corners_Track.parquet")
    save_parquet(TrackApexDeltaData, "apexdelta_Track.parquet")

    Settings["TrackData"] = 0

# Load Voyager Data
if Settings["LoadVoyagerData"] == 1:
    Settings["VoyagerData"] = 1
    setup_file = input("Enter path to Voyager SetupIDs CSV file: ")
    Tracks, SetupIDs = read_csv_column_pairs_from_index(setup_file, start_index=3)

    VoyagerSetupInfo, VoyagerData, VoyagerNumCorners = ImportVoyagerData(Tracks, SetupIDs, Settings)
    VoyagerData, VoyagerApexDeltaData = AppendCornerPhases(Settings, VoyagerSetupInfo, VoyagerData)

    save_parquet(VoyagerSetupInfo, "setup_Voyager.parquet")
    save_parquet(VoyagerData, "data_Voyager.parquet")
    save_parquet(VoyagerNumCorners, "corners_Voyager.parquet")
    save_parquet(VoyagerApexDeltaData, "apexdelta_Voyager.parquet")

    Settings["VoyagerData"] = 0
