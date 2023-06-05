# This part of the code prepare data for rotation and filtering 
from datetime import timedelta, datetime
import time
import obspy
import os
import sys

try:
    netwrok_code = str(sys.argv[1])
except IndexError:
    print("you need to insert network code!")
    sys.exit(1)
trim_name = int(sys.argv[2])  # set 1 if you want to trim the name to seconds

base_path = '/Users/hesam/RF/NETWORKS/{network_code}'
station_list = os.listdir(base_path.format(network_code=netwrok_code))
for sta in station_list:
    sta_dir = os.path.join(base_path.format(network_code=netwrok_code),sta,"Seismograms")
    if os.path.isdir(sta_dir):
        ev_list = os.listdir(sta_dir)
    else:
        continue
    
    for comp in ev_list:
        if trim_name:
            st_info = obspy.read(os.path.join(sta_dir,comp))
            if st_info[0].stats.sac['lcalda'] != 1:
                st_info[0].stats.sac['lcalda'] = 1
            chnl= st_info[0].stats["channel"]

            days = int(st_info[0].stats.sac['nzjday']) -1  # minus one to correct the year convertion
            refr = timedelta(
                days= days,
                seconds=int(st_info[0].stats.sac['nzsec']),
                minutes=int(st_info[0].stats.sac['nzmin']),
                hours=int(st_info[0].stats.sac['nzhour'])
            )
            origin_diff = timedelta(seconds = int(st_info[0].stats.sac['o']))
            year = datetime(int(st_info[0].stats.sac['nzyear']),1,1,0,0,0)

            # Put the time and difference together as datetime object
            evtime = year + refr + origin_diff
            str_name = "Event_"+evtime.strftime("%Y.%m.%d.%H.%M.%S").rstrip("0")+"."+chnl
            os.remove(os.path.join(sta_dir,comp))
            st_info.write(os.path.join(sta_dir,str_name), format="SAC")
            time.sleep(0.05)
            
        else:  
            st_info = obspy.read(os.path.join(sta_dir,comp))
            if st_info[0].stats.sac['lcalda'] != 1:
                st_info[0].stats.sac['lcalda'] = 1
                st_info.write(os.path.join(sta_dir,comp), format="SAC")
            
        