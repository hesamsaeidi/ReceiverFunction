import os

def make_dir(dir_path):
    if not os.path.isdir(dir_path):
        os.mkdir(dir_path)
        
        

def log_to_file(fileName,logContent):
    with open(fileName, 'a+') as lgf:
        lgf.write(str(logContent)+'\n')    