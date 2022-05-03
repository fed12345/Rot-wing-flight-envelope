import sys
from os import path, getenv

import matplotlib.pyplot as plt

# if PAPARAZZI_HOME not set, then assume the tree containing this
# file is a reasonable substitute


from log_parser import LogParser
from ctrl_eff_est import CtrlEffEst

parsed_log = LogParser('/home/federico/Desktop/logs/211215_windtunnel/15_14_14/80_01_06__05_12_30_SD.data',265, 340) #Roll
#parsed_log = LogParser('/home/federico/Desktop/logs/211217_windtunnel/18_11_21/80_01_06__03_13_04_SD.data',147, 267) #Yaw
#parsed_log = LogParser('/home/federico/Desktop/logs/211215_windtunnel/19_43_21/80_01_06__09_41_19_SD.data',1054, 1225) #Pitch


eff_estimator = CtrlEffEst( parsed_log,\
                            [0.047,0.047,0.047,0.047,0.1,0.1,0.1,0.1,0.047],\
                            1.5,\
                            [[1100., 2000.],[1100.,2000.],[1100.,2000.],[1100.,2000.],[1100.,1900.],[1100.,1900.],[1100.,1900.],[1100.,1900.],[1100., 2000.]],\
                            [0,0,0,0,1,1,1,1,0],\
                            [0,1,2,3,4,5,6,7,8])
'''
eff_estimator = CtrlEffEst( parsed_log,\
                            [0.047,0.047,0.047,0.047],\
                            1.5,\
                            [[1100., 2000.],[1100.,2000.],[1100.,2000.],[1100.,2000.]],\
                            [0,0,0,0],\
                            [0,1,2,3])
'''
eff_estimator.get_effectiveness_values()