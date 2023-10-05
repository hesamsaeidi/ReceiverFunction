import sys
import os
import collections


base_path = '/Users/hesam/RF/NETWORKS'
network_list = os.listdir(base_path)
all_stations = []
unique_stations = set()

for network in network_list:
    data_dir = os.path.join(base_path,network)
    if os.path.isdir(data_dir) and not network.startswith('.'):
        all_stations.extend(os.listdir(data_dir))
        
# create a uniqe list of stations in a set
for sta in all_stations:
    unique_stations.add(sta)
    # print(unique_stations)
    
print(len(unique_stations))     
print(len(all_stations)) 
# return the list of stations that are repeated
print([item for item, count in collections.Counter(all_stations).items() if count > 1])
