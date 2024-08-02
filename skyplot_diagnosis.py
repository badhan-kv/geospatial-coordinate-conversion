import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from math import atan2, sqrt, radians
from xyz_neu import xyz2neu
from xyz_lla import lla2xyz

# Function to calculate azimuth and elevation
def calculate_az_el(neu):
    n, e, u = neu
    hlen = sqrt(n**2 + e**2)
    elevation = atan2(u, hlen)
    azimuth = atan2(e, n)
    return azimuth, elevation

def plot_skyplots(folder_path, lat_ref, lon_ref, alt_ref=0):
    for csvfile in os.listdir(folder_path):
        if csvfile.endswith('.csv'):
            file_path = os.path.join(folder_path, csvfile)
            sat_data = pd.read_csv(file_path)

            az_list = []
            el_list = []

            for _, row in sat_data.iterrows():
                # Compute ground station to satellite vector in XYZ
                neu = xyz2neu(row['x in m'], row['y in m'], row['z in m'], lat_ref, lon_ref, alt_ref)
                az, el = calculate_az_el(neu)

                # Convert radians to degrees
                az_deg = np.degrees(az)
                el_deg = np.degrees(el)

                # Discard if below horizon
                if el_deg > 0:
                    az_list.append(az_deg)
                    el_list.append(90 - el_deg)  # 90 - elevation for zenith angle

            # Plotting
            fig = plt.figure()
            ax = fig.add_subplot(111, polar=True)
            ax.plot(np.radians(az_list), el_list)  # Convert azimuth to radians for plotting
            ax.set_theta_zero_location('N')
            ax.set_theta_direction(-1)
            ax.set_title(f"Skyplot for {csvfile}")

    plt.show()

if __name__ == "__main__":
    folder_path = r'C:\Users\KhushaldasBadhan\OneDrive - ODYSSEUS SPACE\Documents\semester\GNSS\HW4\sat_positions'
    lat_ref = 49.63
    lon_ref = 6.15
    
    plot_skyplots(folder_path, lat_ref, lon_ref)
    
    print("done!")
