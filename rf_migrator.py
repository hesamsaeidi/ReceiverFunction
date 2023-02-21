import sys
import os


data_path = '/Users/hesam/AFRICA'
destin_path = '/Users/hesam/RF/NETWORKS'
station_lst = []
# network name must be inserted as second arg
try:
    network_name = str(sys.argv[1])
except IndexError:
    print("you need to insert network name!")
    sys.exit(1)
    
# test
# print(os.listdir(os.path.join(data_path, netwrok_name)))

network_dir = os.path.join(destin_path,network_name)
data_dir = os.path.join(data_path,network_name)
if os.path.isdir(network_dir):
    print('yes')
else:
    os.mkdir(network_dir)
    print("The directory created!")

ev_dir =[name for name in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, name))]
ev_dir.remove('SCRIPTS')
# print(len(ev_dir,), type(ev_dir))
stations_dir = os.path.join(data_dir,'stationList')
with open(stations_dir) as f:
    for line in f:
        station_lst.append(line.rstrip())
# print(station_lst)
for sta in station_lst:
    # sudo code
    make dir 
    iter data path
    grab ev_name
    copy file with new ev name in sta dir
    move to the next
