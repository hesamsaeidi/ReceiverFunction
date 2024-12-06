# from readmod_func import read_model_data, read_coordinates
import numpy as np
import os
from scipy.interpolate import griddata

minlat, maxlat = -45, 40
minlon, maxlon = 1, 50
mindep, maxdep = 0, 2880

# Define the dtype
dtype = [('index', 'i4'), ('lat', 'f8'), ('lon', 'f8'),
         ('dep', 'f8'), ('vp', 'f8'), ('vs', 'f8')]



# Initialize an empty list to collect filtered data
filtered_data = []

# Function to read the coordinate file


def read_coordinates(coord_file):
    coords = []
    with open(coord_file, 'r') as f:
        for i, line in enumerate(f):
            parts = line.split()
            lat = float(parts[0])
            lon = float(parts[1])
            if minlat <= lat <= maxlat and minlon <= lon <= maxlon:
                coords.append({'index': i + 1, 'lat': lat, 'lon': lon})
    return coords

# Function to read and filter layered data files


def read_layered_data(files, coords):
    global_data = {entry['index']: {'lat': entry['lat'], 'lon': entry['lon'], 'depth': [
    ], 'vp': [], 'vs': []} for entry in coords}

    for file in files:
        with open(file, 'r') as f:
            for i, line in enumerate(f):
                parts = line.split()
                index = i+1 # line number in the reference file
                depth = float(parts[1])
                vp = float(parts[2])
                vs = float(parts[4])

                if index in global_data and mindep < depth <= maxdep:
                    global_data[index]['depth'].append(depth)
                    global_data[index]['vp'].append(vp)
                    global_data[index]['vs'].append(vs)
                    # print(index, global_data[index])

    # Filter out any entries that don't have valid depth, vp, or vs
    filtered_data = []


    for index, entry in global_data.items():
        # print(">>>>>>>>", index, entry)
        for d, vp, vs in zip(entry['depth'], entry['vp'], entry['vs']):
            filtered_data.append(
                (index, entry['lat'], entry['lon'], d, vp, vs))

    return filtered_data
    # return global_data


def interp_grid(key, grid_data):
    inter_dep = np.arange(mindep, maxdep+1, 10)

    inter_lat = np.arange(minlat, maxlat+1)
    inter_lon = np.arange(minlon, maxlon+1)
    new_dep, new_lat, new_lon = np.meshgrid(
        inter_dep, inter_lat, inter_lon, indexing='ij')
    point_num = grid_data.shape[0]
    points = np.zeros([point_num, 3])
    values = np.zeros(point_num)
    for i in range(point_num):
        print(grid_data[i])
        points[i, 0] = grid_data[i]['dep']
        points[i, 1] = grid_data[i]['lat']
        points[i, 2] = grid_data[i]['lon']
        values[i] = grid_data[i][key]
        print(points[i], values[i])
    data = griddata(
        points, values, (new_dep, new_lat, new_lon), method='linear')
    # print(grid_data.shape, new_lat.shape)
    return data, new_dep[:, 0, 0], new_lat[0, :, 0], new_lon[0, 0, :]



# File paths (replace with your actual file paths)
coord_file = 'SPiRaL_1.4_Interpolated/SPiRaL_1.4.Interpolated.Coordinates.txt'

# get the list of the remaining files for the model
model_files = os.listdir('SPiRaL_1.4_Interpolated')
model_files = [file for file in model_files if file.endswith('.txt')]
model_files = [file for file in model_files if 'Coordinates' not in file]
# now I need to add the folder name to each file in this list
model_files = ['SPiRaL_1.4_Interpolated/' + file for file in model_files]
# Read coordinates
coords = read_coordinates(coord_file)
# print("Coordinates read:", coords[:5])  # Debug: print the first 5 coordinates
# Read and filter the layered data
filtered_data = read_layered_data(model_files, coords)

# Initialize the structured array with filtered data
grid_data = np.array(filtered_data, dtype=dtype)



vp, dep, lat, lon = interp_grid('vp', grid_data)
vs, _, _, _ = interp_grid('vs', grid_data)

np.savez('SPiRaL', dep=dep, lat=lat, lon=lon, vp=vp, vs=vs)
