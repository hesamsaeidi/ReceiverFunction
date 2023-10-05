import sys
import os
import glob
import shutil
from nec_func import *

data_path = '/Users/hesam/AFRICA/'
# data_path = '/Users/hesam/RF/From_Sam'
# data_path = '/Users/hesam/AFRICA/Ryan/AFRICA_S'
destin_path = '/Users/hesam/RF/NETWORKS'
station_lst = []
# network name must be inserted as second arg
try:
    network_name = str(sys.argv[1])
except IndexError:
    print("you need to insert network name!")
    sys.exit(1)
    

network_dir = os.path.join(destin_path,network_name)
data_dir = os.path.join(data_path,network_name)
if os.path.isdir(network_dir):
    print('The directory exists!')
else:
    os.mkdir(network_dir)
    print("The directory created!")

ev_dir_lst =[name for name in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, name))]
ev_dir_lst.remove('SCRIPTS')
# print(len(ev_dir_lst,), type(ev_dir_lst))
stations_dir = os.path.join(data_dir,'stationList')
with open(stations_dir) as f:
    for line in f:
        station_lst.append(line.rstrip())
# print(station_lst)
for sta in station_lst:
    sta_dir = os.path.join(network_dir,sta)
    if not os.path.isdir(sta_dir):
        print(sta_dir)
        os.mkdir(sta_dir)
    for ev in ev_dir_lst:
        e_file = glob.glob(os.path.join(data_dir,ev,sta+"*E"))
        n_file = glob.glob(os.path.join(data_dir,ev,sta+"*N"))
        z_file = glob.glob(os.path.join(data_dir,ev,sta+"*Z"))
        
        if e_file and n_file and z_file:
            e_destin_file = os.path.join(sta_dir, "Seismograms", ev+"."+e_file[0][-3:])
            n_destin_file = os.path.join(sta_dir, "Seismograms", ev+"."+n_file[0][-3:])
            z_destin_file = os.path.join(sta_dir, "Seismograms", ev+"."+z_file[0][-3:])
            make_dir(os.path.dirname(e_destin_file))
            shutil.copy2(e_file[0], e_destin_file)
            shutil.copy2(n_file[0], n_destin_file)
            shutil.copy2(z_file[0], z_destin_file)
           