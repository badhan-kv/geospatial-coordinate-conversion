from xyz_lla import xyz2lla
import numpy as np

x, y, z = -25007.62321, 4283.253296, -8225.535973
lat_1, lon_1, alt_1 = xyz2lla(x, y, z)
print("lat_1= ", lat_1, "lon_1= ", lon_1, "alt_1= ", alt_1)