import sys
import os
import subprocess
import shutil
from nec_func import *

iterd = '/Users/hesam/RF/PROGRAMS.330/bin/saciterd'


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
    low_recovery_rf_dir = os.path.join(rf_dir,'Low_Recovery')
    make_dir(low_recovery_rf_dir)
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
                                        # -FN file_num (default none) numerator SAC binary
                                        # -FD file_den (default none) denominator SAC binary
                                        # -E error (0.001) convergence criteria
                                        # -ALP alpha (default 1.0) Gaussian Filter Width  (NOTE: Emry et al. used both 0.5 and 1)
                                        #     H(f) = exp( - (pi freq/alpha)**2) 
                                        #     Filter corner ~ alpha/pi 
                                        # -N niter (default 100, 1000 max) Number iterations/bumps
                                        # -D delay (5 sec) Begin output delay sec before t=0
                                        # -POS (default false) Only permit positive amplitudes
                                        # -2  (default false) use double length FFT to  avoid FFT wrap around in convolution
                                        # -RAYP rayp (default -12345.0) ray parameter in  sec/km used by rftn96/joint96
                                        "-E",'0.0001', "-ALP", "1","-N","500", "-D","0", "-POS","false"],
                                       capture_output=True)
            # print(rf_output)
            # print(rf_output.stderr)
            indx = rf_output.stdout.decode("utf-8").find('The final deconvolution reproduces')
            recovery_percent = float(rf_output.stdout.decode("utf-8")[indx+34:indx+41].strip())
            log_file = os.path.join(rf_dir,'decon_recovery.log')
            log_to_file(log_file,stream_name[:-3]+rf_output.stdout.decode("utf-8")[indx+34:indx+42])
            if recovery_percent > 79:
                shutil.copy2('decon.out', os.path.join(rf_dir,stream_name+'decon.out'))
            else:
                print('no files will be created!')
                shutil.copy2('decon.out', os.path.join(low_recovery_rf_dir,stream_name+'decon.out'))
            os.remove('denominator')
            os.remove('numerator')
            os.remove('observed')
            os.remove('predicted')
            
        break
    break    
        
    
