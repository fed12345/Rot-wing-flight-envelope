#Merge all the flights in diffrenet categories depending on the angle of the wing and apply a filter to remove noise from data
# Also store the data in a folder

from xml.etree.ElementInclude import default_loader
import numpy as np
import scipy as sp
from scipy import signal
import matplotlib.pyplot as plt
import pickle as pk
import csv
import os 
import pandas as pd
import tkinter as tk

from log_parser.flight_env import FlightEnv

from statsmodels.nonparametric.smoothers_lowess import lowess

from tkinter import filedialog




#Plotting
from mpl_toolkits import mplot3d
import mpl_scatter_density
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.pyplot as plt

white_viridis = LinearSegmentedColormap.from_list('white_viridis', [
    (0, '#ffffff'),
    (1e-20, '#440053'),
    (0.2, '#404388'),
    (0.4, '#2a788e'),
    (0.6, '#21a784'),
    (0.8, '#78d151'),
    (1, '#fde624'),
], N=256)

def unpickle(file):
    """Unpickle file

    Args:
        file (pk): pickled file

    Returns:
        dict (dic): Return ditionary of file 
    """

    with open(file, 'rb') as f:
        dict = pk.load(f)
    return dict
class Flightmerge():
    """
    Merge all flights in a folder
    """    
    def __init__(self, only_plot = False, *inputdir):
        if only_plot == False:
            if len(inputdir)==0:
                root = tk.Tk()
                self.folder_path = tk.filedialog.askdirectory(title = 'Select Flight Data Folder')
                root.withdraw()
            else:
                self.folder_path = inputdir
            self.all90fligths = { 'airspeed': [], 'acc_z' : [],'airspeed_f': [], 'acc_z_f' : [], 'wing_angle_deg': [], 'ref_acc_z': [], 'u' : [],'ap_mode' : []}
            self.all80fligths = {'airspeed': [], 'acc_z' : [],'airspeed_f': [], 'acc_z_f' : [],'wing_angle_deg': [], 'ref_acc_z': [], 'u' : [],'ap_mode' : []}
            self.all40fligths = {'airspeed': [], 'acc_z' : [],'airspeed_f': [], 'acc_z_f' : [], 'wing_angle_deg': [], 'ref_acc_z': [], 'u' : [],'ap_mode' : []}
            self.all0fligths = {'airspeed': [], 'acc_z' : [] ,'airspeed_f': [], 'acc_z_f' : [], 'wing_angle_deg': [], 'ref_acc_z': [], 'u' : [],'ap_mode' : []}
            
        else:
            self.all90fligths = unpickle("/Users/Federico/Desktop/Rotating_wing/filtered_data/all90fligths.pkl")
            self.all80fligths = unpickle("/Users/Federico/Desktop/Rotating_wing/filtered_data/all80fligths.pkl")
            self.all40fligths = unpickle("/Users/Federico/Desktop/Rotating_wing/filtered_data/all40fligths.pkl")
            self.all0fligths = unpickle("/Users/Federico/Desktop/Rotating_wing/filtered_data/all0fligths.pkl")
            self.plotter(2)


    def merger(self):       
        files = os.listdir(self.folder_path)
        count = 0
        for f in files:
            if f == '.DS_Store':
                continue
            data_path = os.path.join(self.folder_path, f)
            count += 1
            print(count/len(files)*100)
            print(data_path)
            flight = FlightEnv(data_path)
            flight90, flight80, flight40, flight0 = flight.wing_angle_parser()

            
            if len(flight90['acc_z']) > 0:
                flight90_f = self.filter(flight90, 0.6)
                self.all90fligths['airspeed_f'].extend(flight90_f[:,0])
                self.all90fligths['acc_z_f'].extend(flight90_f[:,1]) 
                self.all90fligths['airspeed'].extend(flight90['airspeed'])
                self.all90fligths['acc_z'].extend(flight90['acc_z'])
                self.all90fligths['wing_angle_deg'].extend(flight90['wing_angle_deg_sp'])
                self.all90fligths['ref_acc_z'].extend(flight90['ref_acc_z'])
                self.all90fligths['u'].extend(flight90['u'])
                self.all90fligths['ap_mode'].extend(flight90['ap_mode'])


            if len(flight80['acc_z']) > 0:
                flight80_f = self.filter(flight80, 0.6)
                self.all80fligths['airspeed_f'].extend(flight80_f[:,0])
                self.all80fligths['acc_z_f'].extend(flight80_f[:,1]) 
                self.all80fligths['airspeed'].extend(flight80['airspeed'])
                self.all80fligths['acc_z'].extend(flight80['acc_z'])
                self.all80fligths['wing_angle_deg'].extend(flight80['wing_angle_deg_sp']) 
                self.all80fligths['ref_acc_z'].extend(flight80['ref_acc_z'])
                self.all80fligths['u'].extend(flight80['u'])
                self.all80fligths['ap_mode'].extend(flight80['ap_mode'])



            if len(flight40['acc_z']) > 0:
                flight40_f = self.filter(flight40, 0.6)
                self.all40fligths['airspeed_f'].extend(flight40_f[:,0])
                self.all40fligths['acc_z_f'].extend(flight40_f[:,1]) 
                self.all40fligths['airspeed'].extend(flight40['airspeed'])
                self.all40fligths['acc_z'].extend(flight40['acc_z'])
                self.all40fligths['wing_angle_deg'].extend(flight40['wing_angle_deg_sp'])
                self.all40fligths['ref_acc_z'].extend(flight40['ref_acc_z'])
                self.all40fligths['u'].extend(flight40['u'])
                self.all40fligths['ap_mode'].extend(flight40['ap_mode'])


            
            if len(flight0['acc_z']) > 0:
                flight0_f = self.filter(flight0, 0.6)
                self.all0fligths['airspeed_f'].extend(flight0_f[:,0])
                self.all0fligths['acc_z_f'].extend(flight0_f[:,1]) 
                self.all0fligths['airspeed'].extend(flight0['airspeed'])
                self.all0fligths['acc_z'].extend(flight0['acc_z'])
                self.all0fligths['wing_angle_deg'].extend(flight0['wing_angle_deg_sp'])
                self.all0fligths['ref_acc_z'].extend(flight0['ref_acc_z'])
                self.all0fligths['u'].extend(flight0['u'])
                self.all0fligths['ap_mode'].extend(flight0['ap_mode'])


            

    def filter(self, data, frac):
        """Filter data according to 
        Cleveland, W.S. (1979) “Robust Locally Weighted Regression and Smoothing Scatterplots”.

        Args:
            data (dictionary): Add dlight dictionary
            frac (float): Value between 0 and 1

        Returns:
            array: coloum 0 is y output, coloum 1 is x output
        """        
        data_f = lowess(data['acc_z'],data['airspeed'],frac = frac, it = 0)
        return data_f

    def bw_filter(self,data):
        b, a = signal.butter(2, 1.5/500, 'low', analog=False)
        data_f = signal.lfilter(b, a, data['airspeed'], axis=0)
        data_f = signal.lfilter(b, a, data['airspeed'], axis=0)
        return data_f
    
    def plotter(self, dimension):
        """Plotting all flights

        Args:
            dimension (int): 2 or 3 depending on if a 2D or 3D graph is required
        """        
     
        if dimension == 2:
            def using_mpl_scatter_density(fig, x, y):
                ax = fig.add_subplot(1, 1, 1, projection='scatter_density')
                density = ax.scatter_density(x, y,dpi=40
                , cmap=white_viridis,vmin = 0, vmax =1500)
                fig.colorbar(density, label='Number of points per pixel')

            fig = plt.figure('Wing angle 0-20')
            using_mpl_scatter_density(fig, self.all0fligths['airspeed_f'],(np.subtract(self.all0fligths['acc_z_f'],self.all0fligths['ref_acc_z'])+9.81))
            plt.xlabel('Airspeed [m/s]')
            plt.ylabel('$\Delta$ Acceleration z [m/s^2]')
            plt.title('Stability plot - Wing angle 0-20 [deg]')

            fig = plt.figure('Wing angle 20-40')
            using_mpl_scatter_density(fig, self.all40fligths['airspeed_f'],(np.subtract(self.all40fligths['acc_z_f'],self.all40fligths['ref_acc_z'])+9.81))
            plt.xlabel('Airspeed [m/s]')
            plt.ylabel('$\Delta$ Acceleration z [m/s^2]')
            plt.title('Stability plot - Wing angle 20-40 [deg]')

            fig = plt.figure('Wing angle 40-80')
            using_mpl_scatter_density(fig, self.all80fligths['airspeed_f'],(np.subtract(self.all80fligths['acc_z_f'],self.all80fligths['ref_acc_z'])+9.81))
            plt.xlabel('Airspeed [m/s]')
            plt.ylabel('$\Delta$ Acceleration z [m/s^2]')
            plt.title('Stability plot - Wing angle 40-80 [deg]')

            fig = plt.figure('Wing angle 80-90')
            using_mpl_scatter_density(fig, self.all90fligths['airspeed_f'],(np.subtract(self.all90fligths['acc_z_f'],self.all90fligths['ref_acc_z'])+9.81))
            plt.xlabel('Airspeed [m/s]')
            plt.ylabel('$\Delta$ Acceleration z [m/s^2]')
            plt.title('Stability plot - Wing angle 80-90 [deg]')

            print(len(self.all0fligths['airspeed_f']))
            print(len(self.all40fligths['airspeed_f']))
            print(len(self.all80fligths['airspeed_f']))
            print(len(self.all90fligths['airspeed_f']))


        if dimension == 3:
            print('Not Yet :-)')

    def store_data(self, folder_path):
        """Store data in a pickle file

        Args:
            folder_path (string): Path to folder
        """        
        
        with open(folder_path+'/' + 'all90fligths' + '.pkl', 'wb') as p:
            pk.dump(self.all90fligths,p)
        with open(folder_path+'/' + 'all80fligths' + '.pkl', 'wb') as p:
            pk.dump(self.all80fligths,p)
        with open(folder_path+'/' + 'all40fligths' + '.pkl', 'wb') as p:
            pk.dump(self.all40fligths,p)
        with open(folder_path+'/' + 'all0fligths' + '.pkl', 'wb') as p:
            pk.dump(self.all0fligths,p)
        



if __name__ == '__main__':
 

    x = Flightmerge(only_plot = True)
    # x.merger()
    # x.store_data('/Users/Federico/Desktop/Rotating_wing/full_filtererd_data')
    # x.plotter(2)
    plt.show()
