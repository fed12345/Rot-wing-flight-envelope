#Define the flight evelope of the rotating wing drone
#Import Packages
import numpy as np
import pickle as pk
import matplotlib.pyplot as plt

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
    std = np.std(dict['acc_z_f'])*-9.81
    stable_flight = {'airspeed': [], 'wing_angle': []}

    for i in range(2,len(dict['airspeed_f'])):
        if dict['acc_z_f'][i] > (-9.81 - 0.2*std) or dict['acc_z_f'][i]< (-9.81 + 2*std) :
            continue
        ave = np.mean(dict['acc_z_f'][i-2:i+2])
        if ave > (-9.81 - 0.2*std) or ave < (-9.81 + 0.2*std) :
            continue

        
        stable_flight['airspeed'].append(dict['airspeed_f'][i])
        stable_flight['wing_angle'].append(dict['wing_angle_deg'][i])

        
    return stable_flight

def main():
    """Main Function
    """  
    #Get dictionary of log file
    flight0 = unpickle("/Users/Federico/Desktop/Rotating_wing/filetered_data/all0fligths.pkl")
    flight40 = unpickle("/Users/Federico/Desktop/Rotating_wing/filetered_data/all40fligths.pkl")
    flight80 = unpickle("/Users/Federico/Desktop/Rotating_wing/filetered_data/all80fligths.pkl")
    flight90 = unpickle("/Users/Federico/Desktop/Rotating_wing/filetered_data/all90fligths.pkl")

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
    plt.show()


main()