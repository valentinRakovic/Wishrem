#!/usr/bin/python3
# -*- coding: utf-8 -*-

from __future__ import print_function
from datetime import date, datetime, timedelta
import mysql.connector
import os

__author__ = "Valentin Rakovic"
__copyright__ = "Copyright (c) 2017, Faculty of Electrical Engineering and Information Technologies, UKIM, Skopje, Macedonia"
__version__ = "0.1.0"
__email__ = "{valentin}@feit.ukim.edu.mk"


#get pathloss model for a given channel form DB
def get_pathloss_model(channel):

	host_env = os.getenv('MYSQL_ENV', 'localhost')
	cnx = mysql.connector.connect(user='root',password='rem', host=host_env,database='remdb')
	cursor = cnx.cursor()

	query = ("select L0, alpha, sigma, d0 from propagation_model where channel = " +str(channel)+ " order by timestamp DESC limit 1")

	cursor.execute(query)
	channel_model = dict();
	rows = cursor.fetchone()

	if rows is None:
		channel_model['L0'] = 'none'
		
	else:
		channel_model['L0'] = rows[0]
		channel_model['alpha'] = rows[1]
		channel_model['sigma'] = rows[2]		
		channel_model['d0'] = rows[3] 
		
	cursor.close()
	cnx.close()


	return channel_model; 


#get pathloss model form DB --> obsolete for now. maybe can be used for the future, if per device filtering is required
def get_channel_model(links, channel, timespan):

	host_env = os.getenv('MYSQL_ENV', 'localhost')
	cnx = mysql.connector.connect(user='root',password='rem', host=host_env,database='remdb')
	cursor = cnx.cursor()
	
	stopdate = datetime.now()
	startdate = stopdate-timedelta(minutes=timespan)

	query = ("select if (sum_cnt>"+str(links)+", sum_cnt, 0) from (select sum(cnt) as sum_cnt from (select tx_mac_address, count(distinct rx_mac_address) as cnt from (select * from propagation_model where channel = "+str(channel)+" and timestamp between '"+str(startdate)+"' and '"+str(stopdate)+"') tmptb group by tx_mac_address) temtab) sumtab;")

	cursor.execute(query)

	sum_cnt = cursor.fetchone();

	channel_model = dict();

	if sum_cnt[0] > 0:
		query = ("select avg(L0), avg(alpha) from propagation_model;")		
		cursor.execute(query)
		
		rows = cursor.fetchone()

		if rows is None:
			channel_model['L0'] = 'none'
		
		else:
			channel_model['L0'] = rows[0]
			channel_model['alpha'] = rows[1]
	else:
		print("nema uslovi")
		channel_model['L0'] = 'none'
		
	cursor.close()
	cnx.close()


	return channel_model; 




#get all active transmiter locations from DB
def get_tx_locations(channel, floor, timespan):

	host_env = os.getenv('MYSQL_ENV', 'localhost')
	cnx = mysql.connector.connect(user='root',password='rem', host=host_env,database='remdb')
	cursor = cnx.cursor()

	stopdate = datetime.now()
	startdate = stopdate-timedelta(minutes=timespan)

	query = ("select tx_mac_address, x_coord, y_coord, global_loc_id, tx_power from estimated_locations where floor = "+str(floor)+" and channel = "+str(channel)+" and timestamp between '"+str(startdate)+"' and '"+str(stopdate)+"';")

	cursor.execute(query)
	tx_loc = cursor.fetchall()		
		
	cursor.close()
	cnx.close()


	return tx_loc; 


#get channel status (idle or ocupied) from DB
def get_channel_status(channel, threshold, timespan):

	host_env = os.getenv('MYSQL_ENV', 'localhost')
	cnx = mysql.connector.connect(user='root',password='rem', host=host_env,database='remdb')
	cursor = cnx.cursor()

	stopdate = datetime.now()
	startdate = stopdate-timedelta(minutes=timespan)

	query = ("select if(avg_val>"+str(threshold)+",1,0) from (select avg(value) as avg_val from duty_cycle where channel = "+str(channel)+" and timestamp between '"+str(startdate)+"' and '"+str(stopdate)+"') tmpdb;")

	cursor.execute(query)
	status = cursor.fetchone()		
		
	cursor.close()
	cnx.close()


	return status; 


#get channel status by specific device (idle or ocupied) from DB
def get_channel_status_by_device(channel, rx_add, threshold, timespan):

	host_env = os.getenv('MYSQL_ENV', 'localhost')
	cnx = mysql.connector.connect(user='root',password='rem', host=host_env,database='remdb')
	cursor = cnx.cursor()

	stopdate = datetime.now()
	startdate = stopdate-timedelta(minutes=timespan)

	query = ("select if(avg_val>"+str(threshold)+",1,0) from (select avg(value) as avg_val from duty_cycle where rx_mac_address = '"+rx_add+"' and channel = "+str(channel)+" and timestamp between '"+str(startdate)+"' and '"+str(stopdate)+"') tmpdb;")

	cursor.execute(query)
	status = cursor.fetchone()		
		
	cursor.close()
	cnx.close()


	return status; 


#get status for all channels by device from DB
def get_channel_status_all_by_device(rx_add, threshold, timespan):

	host_env = os.getenv('MYSQL_ENV', 'localhost')
	cnx = mysql.connector.connect(user='root',password='rem', host=host_env,database='remdb')	
	cursor = cnx.cursor()

	stopdate = datetime.now()
	startdate = stopdate-timedelta(minutes=timespan)

	query = ("select channel, if(avg_val>"+str(threshold)+",1,0) from (select channel, avg(value) as avg_val from (select * from duty_cycle where rx_mac_address = '"+str(rx_add)+"' and timestamp between '"+str(startdate)+"' and '"+str(stopdate)+"') tmpdb group by channel) tempdb;")

	cursor.execute(query)
	dc = cursor.fetchall()		
		
	cursor.close()
	cnx.close()


	return dc; 

#get status for all channels from DB
def get_channel_status_all(threshold, timespan):

	host_env = os.getenv('MYSQL_ENV', 'localhost')
	cnx = mysql.connector.connect(user='root',password='rem', host=host_env,database='remdb')
	cursor = cnx.cursor()

	stopdate = datetime.now()
	startdate = stopdate-timedelta(minutes=timespan)

	query = ("select channel, if(avg_val>"+str(threshold)+",1,0) from (select channel, avg(value) as avg_val from (select * from duty_cycle where timestamp between '"+str(startdate)+"' and '"+str(stopdate)+"') tmpdb group by channel) tempdb;")

	cursor.execute(query)
	dc = cursor.fetchall()		
		
	cursor.close()
	cnx.close()


	return dc; 

#get duty cycle from DB
def get_duty_cycle(channel, timespan):

	host_env = os.getenv('MYSQL_ENV', 'localhost')
	cnx = mysql.connector.connect(user='root',password='rem', host=host_env,database='remdb')
	cursor = cnx.cursor()

	stopdate = datetime.now()
	startdate = stopdate-timedelta(minutes=timespan)

	query = ("select value from duty_cycle where channel = "+str(channel)+" and timestamp between '"+str(startdate)+"' and '"+str(stopdate)+"';")

	cursor.execute(query)
	dc = cursor.fetchall()		
		
	cursor.close()
	cnx.close()


	return dc; 


#get duty cycle by device from DB
def get_duty_cycle_by_device(channel, rx_add, timespan):

	host_env = os.getenv('MYSQL_ENV', 'localhost')
	cnx = mysql.connector.connect(user='root',password='rem', host=host_env,database='remdb')
	cursor = cnx.cursor()

	stopdate = datetime.now()
	startdate = stopdate-timedelta(minutes=timespan)

	query = ("select value from duty_cycle where rx_mac_address = '"+rx_add+"' and channel = "+str(channel)+" and timestamp between '"+str(startdate)+"' and '"+str(stopdate)+"';")

	cursor.execute(query)
	dc = cursor.fetchall()		
		
	cursor.close()
	cnx.close()


	return dc; 


#get duty cycle for all channels from DB
def get_duty_cycle_all_channels_by_device(rx_add, timespan):

	host_env = os.getenv('MYSQL_ENV', 'localhost')
	cnx = mysql.connector.connect(user='root',password='rem', host=host_env,database='remdb')
	cursor = cnx.cursor()

	stopdate = datetime.now()
	startdate = stopdate-timedelta(minutes=timespan)

	query = ("select channel, avg(value) from (select * from duty_cycle where rx_mac_address = '"+str(rx_add)+"' and timestamp between '"+str(startdate)+"' and '"+str(stopdate)+"') tmpdb group by channel;")

	cursor.execute(query)
	dc = cursor.fetchall()		
		
	cursor.close()
	cnx.close()


	return dc; 


#get duty cycle for all channels from DB
def get_duty_cycle_all_channels(timespan):

	host_env = os.getenv('MYSQL_ENV', 'localhost')
	cnx = mysql.connector.connect(user='root',password='rem', host=host_env,database='remdb')
	cursor = cnx.cursor()

	stopdate = datetime.now()
	startdate = stopdate-timedelta(minutes=timespan)

	query = ("select channel, avg(value) from (select * from duty_cycle where timestamp between '"+str(startdate)+"' and '"+str(stopdate)+"') tmpdb group by channel;")

	cursor.execute(query)
	dc = cursor.fetchall()		
		
	cursor.close()
	cnx.close()


	return dc; 

