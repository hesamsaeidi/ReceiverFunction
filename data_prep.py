# This part of the code prepare data for rotation and filtering 

import obspy
import os
import sys

try:
    netwrok_code = str(sys.argv[1])
except IndexError:
    print("you need to insert network code!")
    sys.exit(1)

base_path = '/Users/hesam/RF/NETWORKS/{network_code}'
station_list = os.listdir(base_path.format(network_code=netwrok_code))
for sta in station_list:
    sta_dir = os.path.join(base_path.format(network_code=netwrok_code),sta,"Seismograms")
    if os.path.isdir(sta_dir):
        ev_list = os.listdir(sta_dir)
    else:
        continue
    
    for comp in ev_list:
        evinfo = obspy.read(os.path.join(sta_dir,comp))
        if evinfo[0].stats.sac['lcalda'] != 1:
            evinfo[0].stats.sac['lcalda'] = 1
            evinfo.write(os.path.join(sta_dir,comp), format="SAC")
        
        