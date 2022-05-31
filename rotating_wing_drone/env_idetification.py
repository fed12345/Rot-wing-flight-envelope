#Define the flight evelope of the rotating wing drone
#Import Packages
import numpy as np
import pickle as pk
import matplotlib.pyplot as plt
import scipy.signal as sp

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

def stability(dict):
    """Find Stable parts of all flights

    Args:
        dict (dictionary): dictiornary with flight data

    Returns:
        array: array with airspeeds
    """    

    stable_flight = {'airspeed': [], 'wing_angle': []}

    for i in range(1,len(dict['airspeed_f'])):

        if abs(dict['acc_z_f'][i] - (dict['ref_acc_z'][i]-9.80655)) > 0.07 :
            continue
        if abs(np.mean(dict['acc_z'][i-5:i+5]) - (dict['ref_acc_z'][i]-9.81)) > 0.2:
            continue

        
        stable_flight['airspeed'].append(dict['airspeed_f'][i])
        stable_flight['wing_angle'].append(dict['wing_angle_deg'][i])

        
    return stable_flight

def main():
    """Main Function
    """  
    #Get dictionary of log file
    flight0 = unpickle("/Users/Federico/Desktop/Rotating_wing/filtered_data/all0fligths.pkl")
    flight40 = unpickle("/Users/Federico/Desktop/Rotating_wing/filtered_data/all40fligths.pkl")
    flight80 = unpickle("/Users/Federico/Desktop/Rotating_wing/filtered_data/all80fligths.pkl")
    flight90 = unpickle("/Users/Federico/Desktop/Rotating_wing/filtered_data/all90fligths.pkl")

    #Get stable flights
    stable_flight0 = stability(flight0)
    stable_flight40 = stability(flight40)
    stable_flight80 = stability(flight80)
    stable_flight90 = stability(flight90)

    
    


    #Plotting
    plt.figure('Flight Envelope at Load = 1g')
    s=1
    plt.scatter(stable_flight0['airspeed'],stable_flight0['wing_angle'], s = s)
    plt.scatter(stable_flight40['airspeed'],stable_flight40['wing_angle'], s = s)
    plt.scatter(stable_flight80['airspeed'],stable_flight80['wing_angle'], s = s)
    plt.scatter(stable_flight90['airspeed'],stable_flight90['wing_angle'], s = s)
    plt.xlabel('Airspeed [m/s]')
    plt.ylabel('Wing Angle [deg]')
    plt.savefig('/Users/Federico/Desktop/Rotating_wing/flight_envelope_1g.png')
    plt.show()


main()