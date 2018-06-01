# EDGAR DATA READ

## Introduction

The file run.py reads data from a CSV and a .txt file stored in the folder '/input'. Text file contains the length of an idle session. Log.csv contains comma separated values from the publically available data from the SEC. 

The code uses the following modules within python
1) Pandas
2) numpy
3) datetime
4) csv.

## Working
It checks to see if the time of new input is different from time stamp of the previous read. 

If the time stamp remains the same, run.py reads data from the log.csv file. As it reads an ip addresss, it checks within an internal record dataframe to see if it has encountered the ip address before. If it has, it updates the session details for the ip address and proceeds to the next line. If not, it adds a new ip address to the record. 

If the time stamp changes, run.py calls function to write expired sessions. The function writes to a text file 'sessionization.txt' details of a session that expired. run.py then drops those rows from record dataframe and proceeds to read data from log.csv

After reaching the EOF of log.csv, run.py writes onto 'sessionization.txt' the remaining sessions in record and closes the relevant files. 

## Possible Improvements

The python code uses a temporary DataFrame to keep track of ongoing sessions. While easy to work with, they do slow down the code. In future implimentation of the idea different data structures could be used to better suit the real world application. 


### To finish
As I had been travelling while the second round of the Insight fellowship was ongoing, I wasn't able to create a shell file on time. I will be able to do that in the next few days. 
