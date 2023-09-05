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
    
    arrivals = model.get_travel_times(source_depth_in_km=100,
                                  distance_in_degree=45,
                                  phase_list=phase_list)