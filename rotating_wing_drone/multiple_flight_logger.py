import pickle as pk
import matplotlib.pyplot as plt
from tkinter import filedialog
import numpy as np
from scipy import signal
import scipy as sp

#filepath = filedialog.askopenfilename()
filepath = '/home/federico/Desktop/logs/dicts/211215_windtunnel/11_46_14_80_01_06__01_45_47_SD.pkl'
with open(filepath, 'rb') as f:
    x = pk.load(f)


# Loop through variables to be plotted

def plot(dict,msg_name,variable_names = [],idx = []):

    variable_counter = 0
    for variable in variable_names:
        if '[]' in dict[msg_name][variable]['type']:
            for i in idx[variable_counter]:
                if 'unit' in dict[msg_name][variable]:
                    label = variable +'[' + str(i) + ']' + ' ' + dict[msg_name][variable]['unit']
                else:
                    label = variable +'[' + str(i) + ']'
                plt.plot(dict[msg_name]['t'], np.array(dict[msg_name][variable]['data'])[:,i], label=i)

        else:
            # define label
            if 'unit' in dict[msg_name][variable]:
                label = variable + ' ' + dict[msg_name][variable]['unit']
            else:
                label = variable

            plt.plot(dict[msg_name]['t'], dict[msg_name][variable]['data'], label=label)

        variable_counter += 1

    plt.legend()



fig = plt.figure()
#plot(x,'STAB_ATTITUDE_FULL_INDI',['u'], [[0,1,2,3]])
fig.add_subplot(511)
plot(x,'CHIRP', ['axis'])
fig.add_subplot(512)
plot(x,'CHIRP', ['active'])
fig.add_subplot(513)
plot(x,'DOUBLET',['doublet_active'])
fig.add_subplot(514)
plot(x,'ROTORCRAFT_STATUS', ['ap_in_flight'])
#plt.plot(t,airspeed_f)
fig.add_subplot(515)
plot(x,'ROT_WING_CONTROLLER', ['wing_angle_deg_sp'])


  
plt.show()










































# import numpy as np
# import pickle as pk

# # Imports for opening a file from a file dialog
# import tkinter as tk
# from tkinter import filedialog
# import glob as gl
# import os as os
# import sys

# # dictml parser includes
# import dictml.etree.ElementTree as ET

# # Functions for plotter
# import matplotlib.pyplot as plt

# class LogParser(object):
#     def __init__(self, t_start = None, t_end = None):
#         '''
#         Init function for the python LogParser class
#         '''
#         # Copy t_start and t_end
#         self.t_start = t_start
#         self.t_end = t_end

#         # If creating a LogParser object, open a file dialog bodict to open a logile (.data)
#         root = tk.Tk()
#         root.withdraw()
#         folder_path = '/home/federico/Desktop/logs/211221_windtunnel'
#         folders = os.listdir(folder_path)
#         for f in folders:
#             flight_path = os.path.join(folder_path,f)
#             for fil in os.listdir(flight_path):
#                 if fil.endswith('SD.data'):
#                    self.data_path = os.path.join(flight_path, fil)
#                    time = f
#                    break


#             self.log_path  = self.data_path[:-4] + "log"
#             # Parse telemetry message definitions
#             self.msg_definition = {}
#             self.import_message_definitions()

#             # Parse log after log_path is known
#             self.log_dict = {}
#             self.parse_log()
#             with open('/home/federico/Desktop/logs/dicts/' + time +'_'+ self.data_path[-26:-5] + '.pkl', 'wb') as p:
#                 pk.dump(self.log_dict,p)
