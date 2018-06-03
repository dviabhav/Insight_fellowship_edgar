#!/usr/bin/env python3



import pandas as pd
import numpy as np
import os
import csv 
from datetime import datetime as dt
import datetime


########################################################################################################################
####################################################-----FUNCTIONS-----#################################################
########################################################################################################################


def add_new(record,i,row):
    "add a new row to record"
    time=dt.strptime(row[1]+" "+row[2],'%Y-%m-%d %H:%M:%S')
    record.loc[i, ('ip','oc','date_time_start', 'date_time_latest','time_diff')]=(row[0],1, time, time, (time-time).seconds)
    return

def update(record,row):
    "update an already encountered ip address"
    time=dt.strptime(row[1]+" "+row[2],'%Y-%m-%d %H:%M:%S')    #convert string to time format.
    record.loc[record.ip==row[0], ('oc','date_time_latest')]=(record.oc.loc[record.ip==row[0]]+1, time)
    return

def write(record,time,delta_t,f,cond,j):
    "Write to file"
    col=['ip','date_time_start','date_time_latest','time_diff','oc']
    if np.sum(cond):
       # record.loc[cond, ('date_time_latest')]=time
        record.loc[:, ('time_diff')]=record.date_time_latest-record.date_time_start +datetime.timedelta(0,1)  #update the session length for all
        record['time_diff']=record['time_diff'].apply(lambda x : x.seconds)
        record.loc[cond].to_csv(path_or_buf=f,sep=',', columns=col,index=False, header=False,float_format='%g')
    return 

def write_end(record,f,last_datetime):
        "Finish writting data"
        record.loc[:, ('time_diff')]=record.date_time_latest -record.date_time_start  +datetime.timedelta(0,1)
        record['time_diff']=record['time_diff'].apply(lambda x : x.seconds)
        col=['ip','date_time_start','date_time_latest','time_diff','oc']
        record.to_csv(f,sep=',',columns=col,header=False, index=False, float_format='%g')
        
############################################################################################################################    
############################################################################################################################
############################################################################################################################
    

log=open('input/log.csv',newline='')        #opens EDGAR data
data=csv.reader(log)                  #creates a pointer to read rows from EDGAR data.
data.__next__()                         #ignore the first line of header
init=open('input/inactivity_period.txt','r')  #open the text file to read inactivity period
t=int(init.read())                      #read time in seconds

i=0                                     #Ledger
delta_t=datetime.timedelta(0,t)    #time after end of session
record=pd.DataFrame({'ip':'0','oc': [0],'date_time_start': [np.nan],'date_time_latest': [np.nan], 'time_diff':[np.nan]})
last_datetime=np.nan
f=open('output/sessionization.txt',"w+")
#row=next(data)

for row in data:
    time=dt.strptime(row[1]+" "+row[2],'%Y-%m-%d %H:%M:%S')    #read the new time
    flag=(time!=last_datetime)                              #check if new time is differenet from old
    if (np.sum(record.ip==row[0]))==0:           #Check to see if the ip address is new.
        add_new(record,i,row)       #add the ip address to our record
    else:                           #if it has shown up, we update the records
        update(record,row)
    
    if flag:                                                #if the time had changed, we check if session has expired
        cond=(record.date_time_latest+delta_t)<time
        write(record,time,delta_t,f, cond,i)                #write session to file
        record=record.drop(record.loc[cond].index) #delete all sessions which have expired
    
    last_datetime=dt.strptime(row[1]+" "+ row[2], '%Y-%m-%d %H:%M:%S')  #we store last date and time to see if anything changed
    i=i+1


write_end(record,f,last_datetime)
print("File Created")

log.close()
f.close()
