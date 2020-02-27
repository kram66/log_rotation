# ----------------------------------------------------------------------------------------------------------#
# About:		Script to rotate Oracle log files                                                               #
#                                                                                                           #
# Author: 	Mark Young																	                                                  #
# Date:			25/2/2020																	                                                      #
# Why:			Purge .trc and .trm files as well as rotate any file							                              #
#					                                                                                                  #
# History:		V1.0	Initial Code														                                                #
# Requirements:	Python 3																	                                                  #
#				4 parameters														                                                            #
#				create a parameter directory												                                                #
#               Parse the following parameters                                                              #
#               1. Path for log rotation				                                                            #
#               2. File Extension to rotate				                                                          #
#               3. Purge Duration (How long to keep rototated logs before deletion)                         #  
#               4. True/False Should we rotate or not (not if we just want to purge)                        #
#				To rotate the listener log:                                                                         #  
#               python rotatelogs.py E:\App\oraservice\diag\tnslsnr\TQDB10\listener\trace\ log 2            # 
#               python rotatelogs.py E:\App\oraservice\diag\rdbms\dbsid\dbsid\trace\ log 5                  #
#               python rotatelogs.py E:\App\oraservice\diag\rdbms\dbsid\dbsid\trace\ trc 0 False            #
#               python rotatelogs.py E:\App\oraservice\diag\rdbms\dbsid\dbsid\trace\ trm 0 False            #
# ----------------------------------------------------------------------------------------------------------#

import os
import time
from datetime import datetime
import subprocess
import sys
import logging


now = time.time()
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s',
                    filename=r'E:\scripts\logs\Rotation\rotate_logs_' + str(now) + '.log',
                    filemode='w')

try:
    Mylist = str(sys.argv)
    if len(sys.argv) <= 3 :
        logging.error("Please enter 3 arguments")
        sys.exit(1)

    NewExtension = datetime.today().strftime('%m%d%Y')
    MyPath       = sys.argv[1]
    Extension    = sys.argv[2]
    KeepTime     = sys.argv[3]
    Rotate       = sys.argv[4]
    NewPath      = os.path.join(MyPath)
    LogKeep      = 3
    LogDir       = r"E:\scripts\logs\Rotation"
    
    #Before we rename any files, lets remove what we don't want Lets see if there are any files to clean up    
    logging.info("Removing old files.....")
    
    for filename in os.listdir(MyPath):
        if os.path.getmtime(os.path.join(MyPath, filename)) < now - int(KeepTime) * 86400:
            if os.path.isfile(os.path.join(MyPath, filename)):
                logging.info("del " + filename)
                os.remove(os.path.join(MyPath, filename))
     
    if Rotate == "True": 
        #Lets rotate the log, while we are there, we can clean up any files that exceed the keep time    
        logging.info("Rotating log files.....")
        for files in os.listdir(NewPath):
            if files.endswith(Extension):
                logging.info('Rotating log: ', files)
                os.rename(NewPath + files, NewPath + files + '_' + NewExtension)
				
	#Now lets remove any old log files that we have used to keep a record of what we are doing.
    logging.info("Search and destroy and old log files.....")
    for filename in os.listdir(LogDir):
        if os.path.getmtime(os.path.join(LogDir, filename)) < now - int(LogKeep) * 86400:
            if os.path.isfile(os.path.join(LogDir, filename)):
                logging.info("del " + filename)
                os.remove(os.path.join(LogDir, filename))
	
except Exception as e:
    logging.error(e)    
else:
    logging.info("complete")
    
