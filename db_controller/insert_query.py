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

#insert devices in DB
def insert_device(data_device):

	host_env = os.getenv('MYSQL_ENV', 'localhost')
	cnx = mysql.connector.connect(user='root',password='rem', host=host_env,database='remdb')
	cursor = cnx.cursor()

	add_device = ("INSERT INTO devices "
               "(mac_address, type, max_power, x_coord, y_coord, global_loc_id, floor, mode, status, active_channel, active_channel_sup) "
               "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
	cursor.execute(add_device, data_device)
	
	# Make sure data is committed to the database
	cnx.commit()

	cursor.close()
	cnx.close()
	return; 

#insert duty cycle in DB
def insert_duty_cycle(data_duty_cycle):

	host_env = os.getenv('MYSQL_ENV', 'localhost')
	cnx = mysql.connector.connect(user='root',password='rem', host=host_env,database='remdb')
	cursor = cnx.cursor()

	add_duty_cycle = ("INSERT INTO duty_cycle "
               "(rx_mac_address, value, timestamp, channel) "
               "VALUES (%s, %s, %s, %s)")
	cursor.execute(add_duty_cycle, data_duty_cycle)
	
	# Make sure data is committed to the database
	cnx.commit()

	cursor.close()
	cnx.close()
	return;

#insert tx estimated location in DB
def insert_tx_location(data_tx_location):

	host_env = os.getenv('MYSQL_ENV', 'localhost')
	cnx = mysql.connector.connect(user='root',password='rem', host=host_env,database='remdb')
	cursor = cnx.cursor()

	add_tx_location = ("INSERT INTO estimated_locations "
               "(tx_mac_address, x_coord, y_coord, global_loc_id, floor, timestamp, channel, tx_power) "
               "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")
	cursor.execute(add_tx_location, data_tx_location)
	
	# Make sure data is committed to the database
	cnx.commit()

	cursor.close()
	cnx.close()
	return;


#insert propagation model in DB
def insert_propagation_model(data_prop_model):

	host_env = os.getenv('MYSQL_ENV', 'localhost')
	cnx = mysql.connector.connect(user='root',password='rem', host=host_env,database='remdb')
	cursor = cnx.cursor()

	add_prop_model = ("INSERT INTO propagation_model "
               "(L0, alpha, sigma, d0, timestamp, channel) "
               "VALUES (%s, %s, %s, %s, %s, %s)")
	cursor.execute(add_prop_model, data_prop_model)
	
	# Make sure data is committed to the database
	cnx.commit()

	cursor.close()
	cnx.close()
	return;


#insert rssi measurements in DB
def insert_rssi_measurement(data_rssi):

	host_env = os.getenv('MYSQL_ENV', 'localhost')
	cnx = mysql.connector.connect(user='root',password='rem', host=host_env,database='remdb')
	cursor = cnx.cursor()

	add_rssi = ("INSERT INTO rssi_meas "
               "(tx_mac_address, rx_mac_address, value, timestamp, signal_type, bw_mode, active_channel, active_channel_sup) "
               "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")
	cursor.execute(add_rssi, data_rssi)
	
	# Make sure data is committed to the database
	cnx.commit()

	cursor.close()
	cnx.close()
	return;


#insert global point location in DB
def insert_global_location(data_location):
	
	host_env = os.getenv('MYSQL_ENV', 'localhost')
	cnx = mysql.connector.connect(user='root',password='rem', host=host_env,database='remdb')
	cursor = cnx.cursor()

	add_location = ("INSERT INTO global_location "
               "(x_coord, y_coord, z_coord) "
               "VALUES (%s, %s, %s)")
	cursor.execute(add_location, data_location)
	
	# Make sure data is committed to the database
	cnx.commit()

	cursor.close()
	cnx.close()
	return;



