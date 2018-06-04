#!/usr/bin/python
import os
import sys 
import json
import datetime
import math
import time
import threading
import shlex, subprocess
import signal
import requests
from requests.auth import HTTPBasicAuth
import MySQLdb

servers = []

class Analyzer(threading.Thread):
  
  def __init__(self, threadID):
    threading.Thread.__init__(self)
    self.threadID = threadID

  def run(self):
    #global servers
    db = MySQLdb.connect("localhost","root","trungpv92","eATF")
    while True:
	_Read_DCNets(db, '00:00:00:00:00:00:01', '192.168.0.1')
	time.sleep(3.0)


class StatisticCollector(threading.Thread):
	def __init__(self, threadID, DeviceID):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.DeviceID = DeviceID 	#of:0000000000000008 - DeviceID

	def run(self):
	    #global servers
	    db = mariadb.connect(user='root', password='pvtrung92', database='eATF')
		while True:
			url = 'http://localhost:8181/onos/v1/flows/' + self.DeviceID
			headers  = {"Accept": "application/json"}
			response = requests.get(url, headers = headers, auth=HTTPBasicAuth('karaf', 'karaf'))
			print ' ',self.DeviceID,': ',len(response.json()['flows'])
			time.sleep(3.0)

	  		

def _Insert_Statistics(db, value_list):
  # prepare a cursor object using cursor() method
  cursor = db.cursor()
  sql = "INSERT INTO SDDC(MAC, IPAdd, Service, Connected_Device, f_upperbound, bps_upperbound) \
       VALUES ('%s', '%s', '%s', '%s', '%s', '%s')" % \
       (value_list[0], value_list[1], value_list[2], value_list[3], value_list[4], value_list[5])
  try:
     # Execute the SQL command
     cursor.execute(sql)
     # Commit your changes in the database
     db.commit()
  except:
     # Rollback in case there is any error
     db.rollback()
  #db.close()

def _Update_Statistic(db, Acc_ID, value_list):
  # prepare a cursor object using cursor() method
  cursor = db.cursor()
  sql = "UPDATE KeyStorage SET Public_key = '%s', Private_key = '%s' WHERE Acc_ID = '%s'" % (value_list[0], value_list[1], Acc_ID)
  try:
     # Execute the SQL command
     cursor.execute(sql)
     # Commit your changes in the database
     db.commit()
  except:
     # Rollback in case there is any error
     db.rollback()
  #db.close()

def _Read_DCNets(db, MAC, IPAdd):
  # prepare a cursor object using cursor() method
  cursor = db.cursor()
  sql = "SELECT * FROM DCNets WHERE MAC = '%s' AND IPAdd = '%s'" % (MAC, IPAdd)
  try:
     # Execute the SQL command
    cursor.execute(sql)
    results = cursor.fetchall()
  except:
     # Rollback in case there is any error
     db.rollback()
  #db.close()
  return results



#Define new StatisticCollector threads for two switches
#Add or remove moer threads depending on your topoligies or desired switches
sw01 = Analyzer(1)
sw02 = Analyzer(2)

#Start threads
sw01.start()
sw02.start()
