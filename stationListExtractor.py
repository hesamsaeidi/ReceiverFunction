import obspy
import os
from nec_func import log_to_file


StationList = '/Users/hesam/RF/NETWORKS/StationList.txt'
base_path = '/Users/hesam/RF/NETWORKS/'
network_list = os.listdir(base_path)
network_list.remove('.DS_Store')
network_list.remove('stationList.txt')
network_list.remove('meta.log')
for network in network_list:
    station_list = os.listdir(os.path.join(base_path,network))
    for station in station_list:
        data_dir = os.path.join(base_path,network,station,'Seismograms')
        if os.path.isdir(data_dir):
            ev_list = os.listdir(data_dir)
            for ev in ev_list:
                if ev.endswith('HE') or ev.endswith('HN') or ev.endswith('HZ'): 
                    st = obspy.read(os.path.join(data_dir,ev))
                    # print(st[0].stats)
                    stla = st[0].stats.sac['stla']
                    stlo = st[0].stats.sac['stlo']
                    logcontent = f'{stlo}' + ' ' + f'{stla}' + ' ' + f'{station}'
                    log_to_file(StationList,logcontent)
                    break
            
            
            
            