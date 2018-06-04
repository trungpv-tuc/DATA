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
      print _Read_DCNets(db, '00:00:00:00:00:00:01', '192.168.0.1')
      time.sleep(3.0)


class StatisticCollector(threading.Thread):
  def __init__(self, threadID, DeviceID):
    threading.Thread.__init__(self)
    self.threadID = threadID
    self.DeviceID = DeviceID  #of:0000000000000008 - DeviceID

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



#Define a new Analyzer thread
ana = Analyzer(1)
#Start threads
ana.start()


#Define new StatisticCollector threads for switches
#Add or remove more Analyzer depending on your topoligies or desired switches

#sw01 = StatisticCollector(1, 'of:0000000000000001')
#sw02 = StatisticCollector(2, 'of:0000000000000002')
#sw03 = Collector(1, 'of:0000000000000003')
#sw04 = Collector(1, 'of:0000000000000004')
#sw05 = Collector(1, 'of:0000000000000005')
#sw06 = Collector(1, 'of:0000000000000006')
#sw07 = Collector(1, 'of:0000000000000007')
#sw08 = Collector(1, 'of:0000000000000008')
#sw09 = Collector(1, 'of:0000000000000009')
#sw10 = Collector(1, 'of:000000000000000a')
#sw11 = Collector(1, 'of:000000000000000b')

#Start threads
#sw01.start()
#sw02.start()
#sw03.start()
#sw04.start()
#sw05.start()
#sw06.start()
#sw07.start()
#sw08.start()
#sw09.start()
#sw10.start()
#sw11.start()
