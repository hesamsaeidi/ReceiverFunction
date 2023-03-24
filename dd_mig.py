# this file should be executed for data directly downloaded from
# pyweed.
# Hesam Saeidi March 2023 hsaeidi@crimson.ua.edu
import os, sys
from obspy import read
from datetime import timedelta, datetime
import shutil
from nec_func import *

# network name must be inserted as second arg
try:
    network_name = str(sys.argv[1])
except IndexError:
    print("you need to insert network name!")
    sys.exit(1)

base_dir = os.path.join('/Users/hesam/RF/NETWORKS',network_name)
list_dir = os.listdir(base_dir)
for trace in list_dir:
    if not os.path.isdir(os.path.join(base_dir,trace)):
        info_list = trace.split('.')
        station_path = os.path.join(base_dir,info_list[1])
        make_dir(station_path)
        destin_path = os.path.join(station_path,'Seismograms')
        make_dir(destin_path)
        st_info = read(os.path.join(base_dir, trace))
        chnl= st_info[0].stats["channel"]
        print(chnl)
        days = int(st_info[0].stats.sac['nzjday']) -1  # minus one to correct the year convertion
        refr = timedelta(
            days= days,
            seconds=int(st_info[0].stats.sac['nzsec']),
            milliseconds=int(st_info[0].stats.sac['nzmsec']),
            minutes=int(st_info[0].stats.sac['nzmin']),
            hours=int(st_info[0].stats.sac['nzhour'])
            )
        origin_diff = timedelta(seconds = int(st_info[0].stats.sac['o']))
        year = datetime(int(st_info[0].stats.sac['nzyear']),1,1,0,0,0)

        # Put the time and difference together as datetime object
        evtime = year + refr + origin_diff
        event_name = "Event_"+evtime.strftime("%Y.%m.%d.%H.%M.%S.%f").rstrip("0")+"."+chnl
        trace_destin = os.path.join(destin_path, event_name)
        trace_source = os.path.join(base_dir, trace)
        shutil.move(trace_source, trace_destin, copy_function=shutil.copy2)

    