import pandas as pd
from xyz_lla import xyz2lla
import plotly.graph_objects as go
import os

def groundtrack(folder_path):
    # Create a figure for the plot
    fig = go.Figure()

    # Iterate over each CSV file in the folder
    for csvfile in os.listdir(folder_path):
        if csvfile.endswith('.csv'):
            file_path = os.path.join(folder_path, csvfile)
            sat_data = pd.read_csv(file_path)

            # Convert the ECEF coordinates to LLA
            lla_coordinates = sat_data.apply(lambda row: xyz2lla(row['x in m'], row['y in m'], row['z in m']), axis=1)
            sat_data[['latitude', 'longitude', 'altitude']] = pd.DataFrame(lla_coordinates.tolist(), index=sat_data.index)

            # Filter data for the Mercator projection range
            sat_data_filtered = sat_data[(sat_data['latitude'] > -80) & (sat_data['latitude'] < 80)]

            # Add to the plot
            fig.add_trace(go.Scattergeo(
                lon = sat_data_filtered['longitude'],
                lat = sat_data_filtered['latitude'],
                mode = 'lines',
                line = dict(width = 2),
                name = csvfile  # Label the track with the file name
            ))

    # Update layout once for all plots
    fig.update_layout(
        title = 'Satellite Ground Tracks',
        geo = dict(
            projection_type='mercator',
            showland = True,
            landcolor = "rgb(243, 243, 243)",
            countrycolor = "rgb(204, 204, 204)",
        ),
    )

    # Display the plot
    fig.show()

if __name__ == "__main__":
    folder_path = r'C:\Users\KhushaldasBadhan\OneDrive - ODYSSEUS SPACE\Documents\semester\GNSS\HW4\sat_positions'
    
    groundtrack(folder_path)
    
    print("done!")
