import os
from obspy import UTCDateTime
from obspy.clients.fdsn import Client
from obspy import read
import time
fdsn_client = Client('IRIS')


network_name ="ZT"
dir_path = os.path.join('/Users/hesam/RF/NETWORKS',network_name)

pre_filt = (0.005, 0.006, 30.0, 35.0)
# eList = os.listdir(dir_path)
with open('ZT_eventList','r') as eL:
    eList = eL.readlines()
with open('ZT_eventList','r') as eLb:
    eListBackup = eLb.readlines() 
for comp in eList:
    comp_addr = os.path.join(dir_path, comp.strip())
    st = read(comp_addr, debug_headers=True)
    ntw = st[0].stats.network
    stn = st[0].stats.station
    chnl = st[0].stats.channel
    btime = UTCDateTime(str(st[0].stats.starttime)[:-1])
    etime = UTCDateTime(str(st[0].stats.endtime)[:-1])

    inv = fdsn_client.get_stations(
        network=ntw, station=stn, channel=chnl,
        starttime=btime, endtime=etime, level='response'
    )
    # print(inv)
    try:
        st.remove_response(inventory=inv, pre_filt=pre_filt)
        st.write(comp_addr, format="SAC")
        time.sleep(0.05)
        eListBackup.remove(comp)
    except Exception as e:
        print(e)   
        print('>>>new file will be created!!!')
    finally:
        with open('ZT_eventList', 'w') as eLupd:
            for item in eListBackup:
                eLupd.write('{}'.format(item)) 
    
    
    