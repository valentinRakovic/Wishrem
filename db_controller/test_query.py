#!/usr/bin/python3
# -*- coding: utf-8 -*-

from __future__ import print_function
from datetime import date, datetime, timedelta
import mysql.connector
import insert_query
import query_data
import propagation_model_estimation
from numpy import matrix
from numpy import linalg
import numpy 


#A = matrix( [[1,2,3],[11,12,13],[21,22,23]]) # Creates a matrix.
#x = matrix( [[1],[2],[3]] )                  # Creates a matrix (like a column vector).
#y = matrix( [[1,2,3]] )                      # Creates a matrix (like a row vector).
#print(A.T)                                    # Transpose of A.
#print(A*x)                                    # Matrix multiplication of A and x.
#print(A.I)                                    # Inverse of A.
#print(linalg.solve(A, x)) 

#print(propagation_model_estimation.get_PL_chann(60*96,9))

#propagation_model_estimation.get_chann_model(60*200,9)




#print(propagation_model_estimation.get_PL_chann_link(60*200,9,'A1:B2:C3:D4:E5:F6','BA:B2:23:D4:E5:96'))

#print(propagation_model_estimation.get_PL_chann_link(60*200,9,'A1:B2:C3:D4:E5:F6','B1:B2:C3:D4:E5:F6'))

#print(propagation_model_estimation.get_PL_chann_link(60*200,9,'A1:B2:C3:D4:E5:F6','AA:B2:23:D4:E5:96'))




#PL = propagation_model_estimation.get_PL_chann(60*96,9)
#a = numpy.zeros(shape=(len(PL),2))
#A = numpy.asmatrix(a)
#print(A)
#B = A.I
#print(B)

#for row in PL:
#	print(row[0],row[1])


#print(PL[0,0],PL[1,0],PL[0,1],PL[1,1])

#print(propagation_model_estimation.get_PL_chann_dev(60*96,9))


#print(propagation_model_estimation.get_PL_link('A1:B2:C3:D4:E5:F6','AA:B2:23:D4:E5:96',60,9))
#print(propagation_model_estimation.get_PL_link('AA:B2:23:D4:E5:96','A1:B2:C3:D4:E5:F6',60,9))


#propagation_model_estimation.get_distance('A1:B2:C3:D4:E5:F6','11:B2:23:D4:E5:F6')

#propagation_model_estimation.get_distance('11:22:33:44:55:66','11:B2:23:D4:E5:F6')

#print(propagation_model_estimation.get_distance('A1:B2:C3:D4:E5:F6','11:22:33:44:55:66'))

#cm = query_data.get_channel_model_link(11, 'B1:B2:C3:D4:E5:F6', 'BA:B2:23:D4:E5:96');
#print(cm['L0'])


#cm = query_data.get_pathloss_model(11)
#print(cm['L0'], cm['alpha'],cm['sigma'] )

#rows = query_data.get_tx_locations(5,1,60*192)

#print(rows)

#print(query_data.get_channel_status(3,90,4))

#print(query_data.get_channel_status(3,90,4))

#print(query_data.get_channel_status_by_device(1,'A1:B2:33:D4:E5:F6',40,100))

#print(query_data.get_duty_cycle(1,60*1))

#print(query_data.get_duty_cycle_by_device(1,'A1:B2:33:D4:E5:F6',15))

#print(query_data.get_duty_cycle_all_channels_by_device('A1:B2:33:D4:E5:F6',60*48))

#print(query_data.get_duty_cycle_all_channels(60*48))

#print(query_data.get_channel_status_all_by_device('A1:B2:33:D4:E5:F6',70,60*48))

#print(query_data.get_channel_status_all(99,60*48))

#device_data = ('A1:B2:C3:D4:E5:F6', 0, 20, 2.11, 5.41, 2, 1, '802.11a',0,3,0) #(macAdd, devType, maxPower, xCoord, yCoord, floor, mode, status, ch1, ch2)
#insert_query.insert_device(device_data)

#dc_data = ('A1:B2:33:D4:E5:F6', 83, datetime.now(), 5) #(macAdd, value, date, ch)
#insert_query.insert_duty_cycle(dc_data)

#loc_data = ('A1:B2:C3:34:E5:F6', 54, 32, 5, 1, datetime.now(), 5, -33)
#insert_query.insert_tx_location(loc_data)

data = ('-55.55', 2.143, 15, 1, datetime.now(), 11) 
insert_query.insert_propagation_model(data)

#data = ('AA:B2:23:D4:E5:96', 'A1:B2:C3:D4:E5:F6', -73, datetime.now(), 'data', 1, 9, 0) #(macAdd, devType, maxPower, xCoord, yCoord, floor, mode, status, ch1, ch2)
#insert_query.insert_rssi_measurement(data)


#data = (234.12345, 14.456789, 456.89056) 
#insert_query.insert_global_location(data)

#stopdate = datetime.now();
#startdate = stopdate-timedelta(minutes=15)
#print(startdate, stopdate)

