this Repo is for storing all the scripts used to prepare the data from their previous format located in their previous directories into a unitary form for future use of Receiver Function calculation
Hesam Saeidi
hsaeidi@crimson.ua.edu
February 20, 2023

The order of execution is:
1. rf_migrator.py for tomo data 
If the data is recently downloaded through pyweed: 
    1.1 removePZ.py {NOTICE: for dd_mig.py data only}
    1.2 dd_mig.py
2. data_prep.py
    the code should be executed as 
    /.>python data_prep.py {network_name} 1/0
    1 will trim the name of the record to seconds
    0 will leave the name as is
3. filter_rot.py
   this file moves seismograms from their previous folder into the new folder named waveforms after rotation.
   It needs 3-component seismogram (ENZ) recorded at each station for each event and moves the rotated (to RTZ) and filtered data to the new address and trim each trace from 10s before P to 110s after P.
4. rf_calc.py
   The main calculation using `saciterd` written by Ligorrıa and Ammon (1999).
   The rest is housekeeping to keep the files based on the percentage recovery. 
5. rf_plot.py   
   This file plots the RFs and saves them in the folder named `RFs` in the same directory as the data.


