import sys
from os import path
import os as os

import matplotlib.pyplot as plt
import tkinter as tk

# if PAPARAZZI_HOME not set, then assume the tree containing this
# file is a reasonable substitute

from log_parser import LogParser
#Select a full day of testing
root = tk.Tk()
root.withdraw()
folder_path = tk.filedialog.askdirectory(title = 'Select Flight Data Folder')
output_dir = tk.filedialog.askdirectory(title = 'Select Output Folder')

folders = os.listdir(folder_path)
for f in folders:
    flight_path = os.path.join(folder_path,f)
    for fil in os.listdir(flight_path):
        if fil.endswith('SD.data'):
            data_path = os.path.join(flight_path, fil)
            print(data_path)
            log = LogParser(data_path)
            log.store_logs(output_dir)
            break