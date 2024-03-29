import os
from obspy.taup import TauPyModel 

def make_dir(dir_path):
    if not os.path.isdir(dir_path):
        os.mkdir(dir_path)
        
        

def log_to_file(fileName,logContent):
    with open(fileName, 'a+') as lgf:
        lgf.write(str(logContent)+'\n')    
        
        
def call_taup(stream, model, phase_list):
    model = TauPyModel(model=model)
    source_depth = stream[0].stats.sac['evdp']/1000 #convert to km
    distance = stream[0].stats.sac['gcarc']
    arrivals = model.get_travel_times(source_depth_in_km=source_depth,
                                  distance_in_degree=distance,
                                  phase_list=phase_list)
    return arrivals
   
   
def relative_trim(stream, arrivals, a, b):
    # trim the input stream with relative times.
    p_arrival = stream[0].stats.starttime + stream[0].stats.sac['o'] + arrivals[0].time
    stream.trim(p_arrival+a, p_arrival+b)
    return stream


def call_trim(streams):
    e_npts = ev_stream[0].stats.npts
    n_npts = ev_stream[1].stats.npts
    if e_npts < n_npts:
        print("trim n comp")
        t1 = ev_stream[0].stats.starttime
        t2 = ev_stream[0].stats.endtime
        ev_stream[1].trim(t1, t2)
    elif e_npts > n_npts:
        print("trim e comp")
        t1 = ev_stream[1].stats.starttime
        t2 = ev_stream[1].stats.endtime
        ev_stream[0].trim(t1, t2)
    else:
        warnings.warn("trimming doesn't fix your problem")