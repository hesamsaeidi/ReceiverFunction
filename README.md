this Repo is for storing all the scripts used to prepare the data from their previous format located in their previous directories into a unitary form for future use of Receiver Function calculation
Hesam Saeidi
hsaeidi@crimson.ua.edu
February 20, 2023

The order of execution is:
1. rf_migrator.py for tomo data and dd_mig.py for recently downloaded data
    1.1 removePZ.py {NOTICE: for dd_mig.py data only}
2. data_prep.py
    the code should be executed as 
    /.>python data_prep.py {network_name} 1/0
    1 will trim the name of the record to seconds
    0 will leave the name as is
3. filter_rot.py
   this file moves seismograms from their previous folder into the new folder named waveforms after rotation.
   It needs 3-component seismogram (ENZ) recorded at each station for each event and moves the rotated (to RTZ) and filtered data to the new address.
4. rf_calc.py
   The main calculation using `saciterd` written by Ligorrıa and Ammon (1999).
   The rest is housekeeping to keep the files based on the percentage recovery. 

