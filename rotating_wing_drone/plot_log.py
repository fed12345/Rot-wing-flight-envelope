import sys
from os import path, getcwd

import matplotlib.pyplot as plt
from tkinter import filedialog

# if PAPARAZZI_HOME not set, then assume the tree containing this
# file is a reasonable substitute
from log_parser import LogParser

data_path = filedialog.askopenfilename(filetypes=[("data log files", ".data")])

parsed_log = LogParser(data_path)
# parsed_log.plot_variable('STAB_ATTITUDE_FULL_INDI', ['angular_rate_q'], [[]])
# parsed_log.plot_variable('STAB_ATTITUDE_FULL_INDI', ['u'], [[8]])
# parsed_log.plot_variable('STAB_ATTITUDE_FULL_INDI', ['u'], [[2]])
# parsed_log.plot_variable('STAB_ATTITUDE_FULL_INDI', ['u'], [[3]])
# parsed_log.plot_variable('ROTORCRAFT_STATUS', ['ap_in_flight'])
# parsed_log.plot_variable('ROTORCRAFT_FP', [ 'psi'])
#parsed_log.plot_variable('STAB_ATTITUDE_FULL_INDI', ['airspeed'])
#parsed_log.plot_variable('IMU_ACCEL_SCALED', ['ax', 'ay', 'az'])
#parsed_log.plot_variable('INDI_G', ['G1_yaw'], [[0,1,2,3,4]])
parsed_log.plot_variable('ROT_WING_CONTROLLER', ['wing_angle_deg_sp'])
plt.show()
