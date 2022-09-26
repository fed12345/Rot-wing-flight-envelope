#Parse the log files getting only the flight time and store them in a folder


import numpy as np
import scipy as sp
from scipy import signal
import matplotlib.pyplot as plt
import pickle as pk
import csv
import os 
import pandas as pd


class FlightEnv(object):
    def __init__(self, file_path):

        #Parising times
        self.filepath = file_path
        self.log_dict = {}
        self.start_time = []
        self.end_time = []
        self.parsing_time_finder()
 

    def parsing_time_finder(self):
        """Find times when drone is flying
        """        

        with open(self.filepath, 'rb') as p:
               self.log_dict = pk.load(p)

        for i in range(1,len(self.log_dict['ROTORCRAFT_STATUS']['ap_in_flight']['data'])):
            if self.log_dict['ROTORCRAFT_STATUS']['ap_in_flight']['data'][i] == 1 and self.log_dict['ROTORCRAFT_STATUS']['ap_in_flight']['data'][i-1] == 0:
                self.start_time.append(float(self.log_dict['ROTORCRAFT_STATUS']['t'][i]))
            if self.log_dict['ROTORCRAFT_STATUS']['ap_in_flight']['data'][i] == 0 and self.log_dict['ROTORCRAFT_STATUS']['ap_in_flight']['data'][i-1] == 1:
                self.end_time.append(self.log_dict['ROTORCRAFT_STATUS']['t'][i])


    def analize_airspeed(self):
        '''
        For the parsed time find average airspeed, rotated wing angle in order to catalog flight
        '''
        self.flying_dict = {}
        for j in range(len(self.start_time)):
            self.flying_dict.update({j : {"t":[], "airspeed": [], 'wing_angle_deg_sp': [], 'yaw_rate': [], 'roll_rate': [],'pitch_rate': []}})
            for i in range(len(self.log_dict['STAB_ATTITUDE_FULL_INDI']['airspeed']['data'])):
                if self.log_dict['STAB_ATTITUDE_FULL_INDI']['t'][i] < self.start_time[j]:
                    i += 2
                    continue
                if self.log_dict['STAB_ATTITUDE_FULL_INDI']['t'][i] > self.end_time[j]:
                    continue

                     
                self.flying_dict[j]['airspeed'].append(self.log_dict['STAB_ATTITUDE_FULL_INDI']['airspeed']['data'][i])
                self.flying_dict[j]['t'].append(self.log_dict['STAB_ATTITUDE_FULL_INDI']['t'][i])
                self.flying_dict[j]['wing_angle_deg_sp'].append(self.log_dict['ROT_WING_CONTROLLER']['wing_angle_deg_sp']['data'][i])
                self.flying_dict[j]['yaw_rate'].append(self.log_dict['STAB_ATTITUDE_FULL_INDI']['angular_rate_r']['data'][i])
                self.flying_dict[j]['roll_rate'].append(self.log_dict['STAB_ATTITUDE_FULL_INDI']['angular_rate_p']['data'][i])
                self.flying_dict[j]['pitch_rate'].append(self.log_dict['STAB_ATTITUDE_FULL_INDI']['angular_rate_q']['data'][i])
        
    def wing_angle_parser(self):
        """Parse flight accourding to angle of rotating wing

        Returns:
            tuple: flight90, flight80, flight40, flight0
        """        
        flight90 = {'t':[], 'airspeed': [], 'acc_z' : [], 'wing_angle_deg_sp': [], 'ref_acc_z' : [], 'u' : [], 'ap_mode' : [] }
        flight80 = {'t':[], 'airspeed': [], 'acc_z' : [], 'wing_angle_deg_sp': [], 'ref_acc_z' : [],'u' : [], 'ap_mode' : [] }
        flight40 = {'t':[], 'airspeed': [], 'acc_z' : [], 'wing_angle_deg_sp': [], 'ref_acc_z' : [],'u' : [], 'ap_mode' : [] }
        flight0  = {'t':[], 'airspeed': [], 'acc_z' : [], 'wing_angle_deg_sp': [], 'ref_acc_z' : [],'u' : [], 'ap_mode' : [] }

        try:
            self.log_dict['STAB_ATTITUDE_FULL_INDI']['airspeed']['data']           
        except KeyError:
            name = 'EFF_FULL_INDI'
        else:
            name = 'STAB_ATTITUDE_FULL_INDI'

        feqd = len(self.log_dict['GUIDANCE_INDI_HYBRID']['sp_accel_z']['data'])/len(self.log_dict[name]['airspeed']['data'])
        feqd_wing = len(self.log_dict['ROT_WING_CONTROLLER']['wing_angle_deg_sp']['data'])/len(self.log_dict[name]['airspeed']['data'])
        feqd_status = len(self.log_dict['ROTORCRAFT_STATUS']['ap_mode']['data'])/len(self.log_dict[name]['airspeed']['data'])
        for j in range(len(self.start_time)):
            for i in range(len(self.log_dict[name]['airspeed']['data'])):
                if self.log_dict[name]['t'][i] < self.start_time[j]:
                    i += 2
                    continue
                if self.log_dict[name]['t'][i] > self.end_time[j]:
                    continue
        
                if  80 <= self.log_dict['ROT_WING_CONTROLLER']['wing_angle_deg_sp']['data'][int(i*feqd_wing)] <90:
                    flight90['airspeed'].append(self.log_dict[name]['airspeed']['data'][i])
                    flight90['t'].append(self.log_dict[name]['t'][i])
                    flight90['acc_z'].append(self.log_dict[name]['body_accel_z']['data'][i])
                    flight90['wing_angle_deg_sp'].append(self.log_dict['ROT_WING_CONTROLLER']['wing_angle_deg_sp']['data'][int(i*feqd_wing)])
                    flight90['ref_acc_z'].append(self.log_dict['GUIDANCE_INDI_HYBRID']['sp_accel_z']['data'][int(i*feqd)])
                    flight90['u'].append(self.log_dict[name]['u']['data'][i])
                    flight90['ap_mode'].append(self.log_dict['ROTORCRAFT_STATUS']['ap_mode']['data'][int(i*feqd_status)])


                if 40 <= self.log_dict['ROT_WING_CONTROLLER']['wing_angle_deg_sp']['data'][int(i*feqd_wing)] <80:
                    flight80['airspeed'].append(self.log_dict[name]['airspeed']['data'][i])
                    flight80['t'].append(self.log_dict[name]['t'][i])
                    flight80['acc_z'].append(self.log_dict[name]['body_accel_z']['data'][i])
                    flight80['wing_angle_deg_sp'].append(self.log_dict['ROT_WING_CONTROLLER']['wing_angle_deg_sp']['data'][int(i*feqd_wing)])
                    flight80['ref_acc_z'].append(self.log_dict['GUIDANCE_INDI_HYBRID']['sp_accel_z']['data'][int(i*feqd)])
                    flight80['u'].append(self.log_dict[name]['u']['data'][i])
                    flight80['ap_mode'].append(self.log_dict['ROTORCRAFT_STATUS']['ap_mode']['data'][int(i*feqd_status)])


                if 20 <= self.log_dict['ROT_WING_CONTROLLER']['wing_angle_deg_sp']['data'][int(i*feqd_wing)] < 40:
                    flight40['airspeed'].append(self.log_dict[name]['airspeed']['data'][i])
                    flight40['t'].append(self.log_dict[name]['t'][i])
                    flight40['acc_z'].append(self.log_dict[name]['body_accel_z']['data'][i])
                    flight40['wing_angle_deg_sp'].append(self.log_dict['ROT_WING_CONTROLLER']['wing_angle_deg_sp']['data'][int(i*feqd_wing)])
                    flight40['ref_acc_z'].append(self.log_dict['GUIDANCE_INDI_HYBRID']['sp_accel_z']['data'][int(i*feqd)])
                    flight40['u'].append(self.log_dict[name]['u']['data'][i])
                    flight40['ap_mode'].append(self.log_dict['ROTORCRAFT_STATUS']['ap_mode']['data'][int(i*feqd_status)])

                
                if 0 <= self.log_dict['ROT_WING_CONTROLLER']['wing_angle_deg_sp']['data'][int(i*feqd_wing)] < 20:
                    flight0['airspeed'].append(self.log_dict[name]['airspeed']['data'][i])
                    flight0['t'].append(self.log_dict[name]['t'][i])
                    flight0['acc_z'].append(self.log_dict[name]['body_accel_z']['data'][i])
                    flight0['wing_angle_deg_sp'].append(self.log_dict['ROT_WING_CONTROLLER']['wing_angle_deg_sp']['data'][int(i*feqd_wing)])
                    flight0['ref_acc_z'].append(self.log_dict['GUIDANCE_INDI_HYBRID']['sp_accel_z']['data'][int(i*feqd)])
                    flight0['u'].append(self.log_dict[name]['u']['data'][i])
                    flight0['ap_mode'].append(self.log_dict['ROTORCRAFT_STATUS']['ap_mode']['data'][int(i*feqd_status)])



        return flight90, flight80, flight40, flight0

    def bw_filter(self,data,order, wn):
        b, a = signal.butter(2, 1.5/500, 'low', analog=False)
        data_f = signal.lfilter(b, a, data, axis=0)
        return data_f

    def write_csv(self,csv_file):
        """Writes log in csv one line 

        Args:
            csv_file (path): Path to csv file
        """        
        writer = csv.writer(csv_file)
        name = self.filepath[-34:-7]
        day = self.filepath[-52:-35]

        for i in range(len(self.flying_dict)):
        
            airspeed_f = self.bw_filter(self.flying_dict[i]['airspeed'], 2, 1/3000)
            airspeed_mean_entry = np.mean(airspeed_f)
            airspeed_max_entry =  np.max(airspeed_f)
            var_yaw = np.var(self.flying_dict[i]['yaw_rate'])/ abs(np.mean(self.flying_dict[i]['yaw_rate']))
            var_pitch = np.var(self.flying_dict[i]['pitch_rate'])/ abs(np.mean(self.flying_dict[i]['pitch_rate']))
            var_roll = np.var(self.flying_dict[i]['roll_rate'])/ abs(np.mean(self.flying_dict[i]['roll_rate']))

            wing_angle_mean = np.mean(self.flying_dict[i]['wing_angle_deg_sp'])
            if 0 < wing_angle_mean < 8:
                wing_angle_entry = 0
            elif 75 < wing_angle_mean < 90:
                wing_angle_entry = 1
            else:
                wing_angle_entry = 2
            
            writer.writerow([day,name, i, round(airspeed_mean_entry,2), round(airspeed_max_entry,2),wing_angle_entry, round(self.start_time[i],2),round(self.end_time[i],2), round(var_yaw,2),round(var_pitch,2),round(var_roll,2)])

        


            
if __name__ == '__main__':

    log = FlightEnv('/Users/Federico/Desktop/Rotating_wing/logs_reduced/220208_wintunnel_tuning_flightplan_17_49_17_80_01_12__03_38_49_SD.pkl')
    dicts = log.wing_angle_parser()
    '''
    f = open('/Users/Federico/Desktop/Rotating_wing/Code/flights.csv', 'w')
    w = csv.writer(f)
    headers = ["Day","Time_stamp", "Instance", "Airspeed", "Max_airspeed", "Flight_mode", "Start_time", "End_time","Yaw_var","Pitch_var","Roll_var"]
    w.writerow(headers)
    folder_path = '/Users/Federico/Desktop/Rotating_wing/logs_reduced'
    folders = os.listdir(folder_path)
    for s in folders:
        folder_day_path = os.path.join(folder_path,s)
        files = os.listdir(folder_day_path)
        for r in files:
            file_path = os.path.join(folder_day_path,r)
            print(file_path)
            log = FlightEnv(file_path)
        
            log.write_csv(f)
            
    f.close
    '''