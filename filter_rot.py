# This script rotate and filter each 3-componenet seismogram

import obspy
import os
import sys
import warnings
import time
from nec_func import *

try:
    netwrok_code = str(sys.argv[1])
except IndexError:
    print("you need to insert network code!")
    sys.exit(1)

base_path = '/Users/hesam/RF/NETWORKS/{network_code}'
# filtered_data_path = 
# station_list = os.listdir(base_path.format(network_code=netwrok_code))
for sta in station_list:
    sta_dir = os.path.join(base_path.format(network_code=netwrok_code),sta,"Seismograms")
    if os.path.isdir(sta_dir):
        ev_list = os.listdir(sta_dir)
    else:
        continue
    
    unique_streams = set()
    for comp in ev_list:
        stream_name = comp[:-1]
        if not stream_name in unique_streams: 
            unique_streams.add(stream_name)
            ev_stream = obspy.read(os.path.join(sta_dir,stream_name+"*"))
            # print(ev_stream)
            if len(ev_stream) != 3: #
                warnings.warn("insufficient number of components!!")
                # print(stream_name)
                continue
            back_azimuth = ev_stream[0].stats.sac['baz']
            try:
                arrivals = call_taup(ev_stream, "AK135", ["P"]) 
                ev_stream = relative_trim(ev_stream, arrivals, -10, 120) 
                ev_stream.detrend(type="demean")
                ev_stream.detrend(type="linear")
                ev_stream.taper(0.05)
                ev_stream.filter("highpass", freq=0.05)
                ev_stream.filter("lowpass", freq=8)
                ev_stream.interpolate(sampling_rate=20)
                ev_stream.rotate(method='NE->RT',back_azimuth=back_azimuth)

            
                # print(ev_stream)
                filtered_data_path = sta_dir.replace("Seismograms", "Waveforms")
                make_dir(filtered_data_path)
                filtered_data = os.path.join(filtered_data_path,stream_name)
                ev_stream[0].write(filtered_data+"Tf", format="SAC")
                time.sleep(0.1)
                ev_stream[1].write(filtered_data+"Rf", format="SAC")
                time.sleep(0.1)
                ev_stream[2].write(filtered_data+"Zf", format="SAC")
                time.sleep(0.1)
                
            except ValueError as e:
                print(e)
                # call_trim(ev_stream)
                # ev_stream.rotate(method='NE->RT',back_azimuth=back_azimuth)
                continue
            
            except IndexError as e:
                print(e)
                # print(ev_stream[0].stats)
                continue
            
        
