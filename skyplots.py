import pandas as pd
import numpy as np
import plotly.graph_objects as go
import os
from xyz_neu import xyz2neu
from xyz_lla import lla2xyz

def skyplot(folder_path, lat_ref, lon_ref, alt_ref=0):
    # Create a figure for the plot
    fig = go.Figure()

    # Iterate over each CSV file in the folder
    for csvfile in os.listdir(folder_path):
        if csvfile.endswith('.csv'):
            file_path = os.path.join(folder_path, csvfile)
            sat_data = pd.read_csv(file_path)

            # Convert the ECEF coordinates to NEU
            neu_coordinates = sat_data.apply(lambda row: xyz2neu(row['x in m'], row['y in m'], row['z in m'], lat_ref, lon_ref, alt_ref), axis=1)
            sat_data[['north', 'east', 'up']] = pd.DataFrame(neu_coordinates.tolist(), index=sat_data.index)

            # Compute azimuth and elevation
            sat_data['hlen'] = np.sqrt(sat_data['north']**2 + sat_data['east']**2)
            sat_data['elevation'] = np.degrees(np.arctan2(sat_data['hlen'], sat_data['up']))
            sat_data['azimuth'] = np.degrees(np.arctan2(sat_data['east'], sat_data['north']))

            # Filter data (elevation >= 0)
            sat_data_filtered = sat_data[sat_data['elevation'] >= 0]

            # Add to the plot
            fig.add_trace(go.Scatterpolar(
                r = 90 - sat_data_filtered['elevation'],  # 90 - elevation for Plotly's polar plot
                theta = sat_data_filtered['azimuth'],
                mode = 'lines',
                line = dict(width = 2),
                name = csvfile.split('.')[0]  # Label the track with the file name without extension
            ))
            
    # Update layout once for all plots
    fig.update_layout(
        title='Satellite Skyplots',
        polar=dict(
            radialaxis=dict(range=[0, 90], angle=45),  # 90 degrees is the horizon
            angularaxis=dict(direction='clockwise', rotation=90)  # Rotate so North is at top
        )
    )


    # Display the plot
    fig.show()

if __name__ == "__main__":
    folder_path = r'C:\Users\KhushaldasBadhan\OneDrive - ODYSSEUS SPACE\Documents\semester\GNSS\HW4\sat_positions'  
    lat_ref = 49.63  # Latitude of ground station
    lon_ref = 6.15   # Longitude of ground station
    
    skyplot(folder_path, lat_ref, lon_ref)
    
    print("done!")
