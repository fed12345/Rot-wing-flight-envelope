#Define the flight evelope of the rotating wing drone
        # <servo NO="0" NEUTRAL="1100" NAME="MOTOR_FRONT" MIN="1000" MAX="2000"/>
        # <servo NO="1" NEUTRAL="1100" NAME="MOTOR_RIGHT" MIN="1000" MAX="2000"/>
        # <servo NO="2" NEUTRAL="1100" NAME="MOTOR_BACK" MIN="1000" MAX="2000"/>
        # <servo NO="3" NEUTRAL="1100" NAME="MOTOR_LEFT" MIN="1000" MAX="2000"/>
        # <servo NO="4" NEUTRAL="1500" NAME="AIL_LEFT" MIN="1100" MAX="1900"/>
        # <servo NO="5" NEUTRAL="1500" NAME="AIL_RIGHT" MIN="1100" MAX="1900"/>
        # <servo NO="6" NEUTRAL="1500" NAME="VTAIL_LEFT" MIN="1100" MAX="1900"/>
        # <servo NO="7" NEUTRAL="1500" NAME="VTAIL_RIGHT" MIN="1100" MAX="1900"/>
        # <servo NO="8" NEUTRAL="1035" NAME="MOTOR_FWD" MIN="1000" MAX="2000"/>
        # <servo NO="9" NEUTRAL="1507" NAME="WING_ROT" MIN="1000" MAX="2000"/>
#Import Packages
from statistics import mean
from tkinter import S
import numpy as np
import pickle as pk
import matplotlib.pyplot as plt
import scipy.signal as sp
from matplotlib.lines import Line2D



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

def stability(dict, find_yaw=False):
    """Find Stable parts of all flights

    Args:
        dict (dictionary): dictiornary with flight data

    Returns:
        array: array with airspeeds
    """    

    stable_flight = {'airspeed': [], 'wing_angle': [], 'motors_on' : []}
    pusher_saturated = {'airspeed': [], 'wing_angle': []}
    yaw_saturated = {'airspeed': [], 'wing_angle': []}

    for i in range(1,len(dict['airspeed_f'])):




        # Check ap_mode not is 13 or 19

        if dict['ap_mode'][i] != 13 and dict['ap_mode'][i] != 19:
            continue
        
        if sum(dict['u'][i][0:9]) == 11000:
            continue

        
        if abs(dict['acc_z_f'][i] - (dict['ref_acc_z'][i]-9.80655)) > 0.50 :
            continue
        if abs(np.mean(dict['acc_z'][i-5:i+5]) - (dict['ref_acc_z'][i]-9.81)) > 0.50:
           continue

        #pusher saturation
        if dict['u'][i][8] > 1950 and dict['airspeed_f'][i]> 13:
            pusher_saturated['airspeed'].append(dict['airspeed_f'][i])
            pusher_saturated['wing_angle'].append(dict['wing_angle_deg'][i])

        if find_yaw:
            #yaw saturation TODO: Check also yaw with props
            if sum(np.array(dict['u'][i-100:i+100])[:,7]) == 380000 or sum(np.array(dict['u'][i-100:i+100])[:,7]) == 220000:
                if dict['u'][i][0] + dict['u'][i][2] > 3500 or dict['u'][i][1] + dict['u'][i][3] > 3500:
                    yaw_saturated['airspeed'].append(dict['airspeed_f'][i])
                    yaw_saturated['wing_angle'].append(dict['wing_angle_deg'][i])


        motors_on = 1
        if  np.sum(np.array(dict['u'][i:i+4])[:, 0:4]) > 17600:
                motors_on = 0
        

           
        stable_flight['airspeed'].append(dict['airspeed_f'][i])
        stable_flight['wing_angle'].append(dict['wing_angle_deg'][i])
        stable_flight['motors_on'].append(motors_on)

        
    return stable_flight, pusher_saturated, yaw_saturated



def main():
    """Main Function
    """  
    #Get dictionary of log file
    flight0 = unpickle("/Users/Federico/Desktop/Rotating_wing/full_filtererd_data/all0fligths.pkl")
    flight40 = unpickle("/Users/Federico/Desktop/Rotating_wing/full_filtererd_data/all40fligths.pkl")
    flight80 = unpickle("/Users/Federico/Desktop/Rotating_wing/full_filtererd_data/all80fligths.pkl")
    flight90 = unpickle("/Users/Federico/Desktop/Rotating_wing/full_filtererd_data/all90fligths.pkl")

    #Get stable flights
    stable_flight0, pusher0_staurated,yaw0_staurated = stability(flight0, find_yaw = True)
    stable_flight40,pusher40_staurated,yaw40_staurated = stability(flight40, find_yaw = True)
    stable_flight80,pusher80_staurated,yaw80_staurated = stability(flight80)
    stable_flight90,pusher90_staurated,yaw90_staurated = stability(flight90)


    #Plotting
    plt.figure('Flight Envelope at Load = 1g')
    s=4
    plt.title('Flight Envelope of Rotating Wing at Load = 1g')
    plt.scatter(stable_flight0['airspeed'],stable_flight0['wing_angle'], c = stable_flight0['motors_on'], s = s, cmap='RdYlBu')
    plt.scatter(stable_flight40['airspeed'],stable_flight40['wing_angle'], c = stable_flight40['motors_on'], s = s,cmap='RdYlBu') 
    plt.scatter(stable_flight80['airspeed'],stable_flight80['wing_angle'], c = stable_flight80['motors_on'], s = s, cmap='RdYlBu')
    plt.scatter(stable_flight90['airspeed'],stable_flight90['wing_angle'], c = stable_flight90['motors_on'], s = s, cmap='RdYlBu')
    plt.scatter(pusher0_staurated['airspeed'],pusher0_staurated['wing_angle'], c = 'black', s = s)
    plt.scatter(pusher40_staurated['airspeed'],pusher40_staurated['wing_angle'], c = 'black', s = s)
    plt.scatter(pusher80_staurated['airspeed'],pusher80_staurated['wing_angle'], c = 'black', s = s)
    plt.scatter(pusher90_staurated['airspeed'],pusher90_staurated['wing_angle'], c = 'black', s = s)
    plt.scatter(yaw0_staurated['airspeed'],yaw0_staurated['wing_angle'], c = 'yellow', s = s)
    plt.scatter(yaw40_staurated['airspeed'],yaw40_staurated['wing_angle'], c = 'yellow', s = s)
    plt.xlabel('Airspeed [m/s]')
    plt.ylabel('Skew [deg]')
    plt.legend(handles=[Line2D([0], [0], marker='o', color='w', label='Motors On',markerfacecolor='r', markersize=10),
                        Line2D([0], [0], marker='o', color='w', label='Motors Off',  markerfacecolor='b', markersize=10),
                        Line2D([0], [0], marker='o', color='w', label='Pusher Saturation',  markerfacecolor='black', markersize=10),
                        Line2D([0], [0], marker='o', color='w', label='Yaw Saturation',  markerfacecolor='yellow', markersize=10)], bbox_to_anchor=(1.04, 1), loc="upper left")
    plt.grid(which='minor', linestyle='--', linewidth=0.5)
    plt.grid(which='major', linestyle='-', linewidth=0.5)
    plt.minorticks_on()
    plt.savefig('/Users/Federico/Desktop/Rotating_wing/flight_envelope_1g', format='png', bbox_inches="tight")
    plt.savefig('/Users/Federico/Desktop/Rotating_wing/flight_envelope_1geps', format='eps', bbox_inches="tight")
    plt.savefig('/Users/Federico/Desktop/Rotating_wing/flight_envelope_1gsvg', format='svg', bbox_inches="tight")


    plt.show()

if __name__ == '__main__':
    main()
