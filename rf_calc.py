import sys
import os
import subprocess
import shutil

iterd = '/Users/hesam/RF/PROGRAMS.330/bin/saciterd'

def make_dir(dir_path):
    if not os.path.isdir(dir_path):
        os.mkdir(dir_path)


try:
    netwrok_code = str(sys.argv[1])
except IndexError:
    print("you need to insert network code!")
    sys.exit(1)


base_path = '/Users/hesam/RF/NETWORKS/{network_code}'
station_list = os.listdir(base_path.format(network_code=netwrok_code))
for sta in station_list:
    data_dir = os.path.join(base_path.format(network_code=netwrok_code),sta,"Waveforms")
    rf_dir = data_dir.replace("Waveforms", "rftn")
    make_dir(rf_dir)
    os.chdir(rf_dir)
    if os.path.isdir(data_dir):
        ev_list = os.listdir(data_dir)
    else:
        continue
    
    unique_streams = set()
    for comp in ev_list:
        stream_name = comp[:-2]
        if not stream_name in unique_streams: 
            unique_streams.add(stream_name)
            r_comp_name = os.path.join(data_dir,stream_name + "Rf")
            z_comp_name = os.path.join(data_dir,stream_name + "Zf")
            rf_output = subprocess.run([iterd , '-FN',r_comp_name , '-FD',z_comp_name, 
                                        "-E",'0.001', "-ALP", "1","-N","200", "-D","0", 
                                        "-POS","false"] ,capture_output=True, shell=True, text=True)
            print(rf_output)
            print(rf_output.stderr)
        break
    break
