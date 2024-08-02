import pandas as pd
from xyz_lla import xyz2lla
import plotly.graph_objects as go

def groundtrack(csvfile):
    # Load the CSV file
    file_path = csvfile
    sat_data = pd.read_csv(file_path)

    # Convert the ECEF coordinates to LLA using the xyz2lla function
    lla_coordinates = sat_data.apply(lambda row: xyz2lla(row['x in m'], row['y in m'], row['z in m']), axis=1)
    sat_data[['latitude', 'longitude', 'altitude']] = pd.DataFrame(lla_coordinates.tolist(), index=sat_data.index)

    # Save the updated data to a new CSV file
    new_csvfile = "converted_" + csvfile
    sat_data.to_csv(new_csvfile, index=False)

    # Check the range of latitude and longitude
    print("Latitude range:", sat_data['latitude'].min(), "to", sat_data['latitude'].max())
    print("Longitude range:", sat_data['longitude'].min(), "to", sat_data['longitude'].max())

    # Sort data by time for proper line continuity
    sat_data.sort_values(by='time', inplace=True)

    # Plotting without filtering
    fig = go.Figure(data=go.Scattergeo(
        lon = sat_data['longitude'],
        lat = sat_data['latitude'],
        mode = 'lines',
        line = dict(width = 2, color = 'blue'),
    ))

    fig.update_layout(
        title = 'Satellite Ground Track',
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
    csvfile = 'sat05.csv'
    groundtrack(csvfile)
    
    print("done!")
