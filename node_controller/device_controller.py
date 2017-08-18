from uniflex.core import modules
import logging
#import datetime
from datetime import date, datetime, timedelta
import time
from uniflex.core import modules
from uniflex.core import events
from uniflex_module_wifi_flex.sensing_events import *
from rrm_events import *
#from uniflex.core.timer import TimerEventSender
import threading
import _thread
from random import randint
import insert_query
import json

__author__ = "Daniel Denkovski"
__copyright__ = "Copyright (c) 2017, Faculty of Electrical Engineering and Information Technologies, UKIM, Skopje, Macedonia"
__version__ = "0.1.0"
__email__ = "{danield}@feit.ukim.edu.mk"

class DeviceController(modules.ControlApplication):
	def __init__(self):
		super(DeviceController, self).__init__()
		self.log = logging.getLogger('DeviceController')
		self.mynodes = {}
		self.myrrm_uuid = None
		self.running = False

	def main_menu(self):
		while (self.running):
			print("Please choose from the selection:")
			print("1. List WiFi devices")
			print("2. Configure WiFi Devices")
			print("0. Quit")
			choice = input(" >>  ")
			if (choice == '0'): 
				self.running = False
				_thread.interrupt_main()
			elif (choice == '1'): self.print_nodes()
			elif (choice == '2'): 
				self.print_nodes()
				numNodes = len(self.mynodes)
				if numNodes:
					print("Which device do you want to configure? ({}-{})".format(1, numNodes))	
					pnode = input(" >>  ")
					if pnode.isdigit() and int(pnode) >= 1 and int(pnode) <= numNodes: 
						nodeind = int(pnode) - 1
						print("Make a selection (1 for monitor, 2 for AP, 3 for station)")
						pmode = input (" >>  ")
						if pmode.isdigit() and int(pnode) >= 1 and int(pnode) <= 3:
							modeind = int(pmode)
							if modeind == 1:
								uuid = list(self.mynodes.keys())[nodeind]
								node = self.mynodes[uuid]
								self.setup_wifi_monitor(node['MAC'])
							if modeind == 2:
								if self.myrrm_uuid:
									uuid = list(self.mynodes.keys())[nodeind]
									node = self.mynodes[uuid]
									macad = node['MAC']				
									rrm_request_event = RRMRequestAPConfiguration(macad)
									self.send_event(rrm_request_event)
								else:
									uuid = list(self.mynodes.keys())[nodeind]
									node = self.mynodes[uuid]
									noChs = len(node['capabilities'])
									if noChs >= 1:
										macad = node['MAC']
										ssid = 'SMARTAP'
										selId = randint(0, noChs-1)
										chnel = list(node['capabilities'])[selId]
										chentry = node['capabilities'][chnel]
										hwmod = 'g'
										if 'g' in chentry['stds']:
											hwmod = 'g'
										elif 'a' in chentry['stds']:
											hwmod = 'a'
										power = chentry['max-tx']
										htcap = None
										self.setup_wifi_ap(macad, ssid, power, chnel, hwmod, htcap)									
							if modeind == 3:
								uuid = list(self.mynodes.keys())[nodeind]
								node = self.mynodes[uuid]
								apindices = self.print_apnodes()
								if (apindices):
									print("Make a selection {}".format(apindices))
									apstr = input (" >>  ")
									if apstr.isdigit() and int(apstr) in apindices:
										apind = int(apstr) - 1
										apuuid = list(self.mynodes.keys())[apind]
										apnode = self.mynodes[apuuid]
										mymac = node['MAC']
										apmac = apnode['MAC']
										ssid = apnode['config']['ssid']
										power = apnode['config']['power']
										channel = apnode['config']['channel']
										self.setup_wifi_station(mymac, ssid, apmac, power, channel)
				else:
					print("No WiFi devices!")
					continue

	def print_nodes(self):
		print("Listing connected WIFi devices... ")
		nodeInd = 1
		for node in self.mynodes:
			mac = self.mynodes[node]['MAC']
			capabilities = self.mynodes[node]['capabilities']
			status = self.mynodes[node]['status']
			details = self.mynodes[node]['details']
			config = self.mynodes[node]['config']
			print("-> WiFi #{}: Status: {}, MAC: {} \n\tConnection: {} \n\tConfiguration: {}".format(nodeInd, status, mac, details, config))
			nodeInd += 1

	def print_apnodes(self):
		print("Listing WiFi AP devices... ")
		nodeInd = 1
		apindices = []
		for node in self.mynodes:
			mac = self.mynodes[node]['MAC']
			capabilities = self.mynodes[node]['capabilities']
			status = self.mynodes[node]['status']
			details = self.mynodes[node]['details']
			config = self.mynodes[node]['config']
			if status == 'AP':
				print("-> AP #{}: MAC: {}, Configuration: {}".format(nodeInd, mac, config))
				apindices.append(nodeInd)
			nodeInd += 1
		return apindices

	@modules.on_start()
	def my_start_function(self):
		self.log.info("start global WiFi controller app")
		self.running = True
		mythread = threading.Thread(target=self.main_menu)
		#mythread.daemon = True
		mythread.start()
		insert_query.device_init()

	@modules.on_exit()
	def my_stop_function(self):
		self.log.info("stop global WiFi controller app")
		self.running = False

	@modules.on_event(events.NewNodeEvent)
	def add_node(self, event):
		node = event.node
		#self.log.info("Added new node: {}, Local: {}".format(node.uuid, node.local))
		self._add_node(node)
		try:
			getcap_event = WiFiGetCapabilities(node.uuid)				
			self.send_event(getcap_event)

		except Exception as e: {}
			#self.log.error("{} Failed, err_msg: {}".format(datetime.datetime.now(), e))

	@modules.on_event(events.NodeExitEvent)
	@modules.on_event(events.NodeLostEvent)
	def remove_node(self, event):
		#self.log.info("Node lost".format())
		node = event.node
		reason = event.reason	
		if self.myrrm_uuid == node.uuid: self.myrrm_uuid = None
		else:
			if node.uuid in self.mynodes: del self.mynodes[node.uuid]
		if self._remove_node(node): {}
			#self.log.info("Node: {}, Local: {} removed reason: {}".format(node.uuid, node.local, reason))

	@modules.on_event(WiFiRssiSampleEvent)
	def serve_rssi_sample_event(self, event):
		receiver = event.node
		data = (event.ta, event.ra, event.rssi, datetime.now(), 'data', 1, event.chnel, 0)
		insert_query.insert_rssi_measurement(data)
		#self.log.info("RSSI: uuid: {}, RA: {}, TA: {}, value: {}, channel: {}".format(receiver.uuid, event.ra, event.ta, event.rssi, event.chnel))

	@modules.on_event(WiFiDutyCycleSampleEvent)
	def serve_duty_cycle_sample_event(self, event):
		receiver = event.node
		dc_data = (event.ra, event.dc*100, datetime.now(), event.chnel)
		insert_query.insert_duty_cycle(dc_data)
		#self.log.info("Duty cycle: uuid: {}, RA: {}, value: {}, channel: {}".format(receiver.uuid, event.ra, event.dc, event.chnel))

	@modules.on_event(WiFiCapabilities)
	def serve_capabilities_event(self, event):
		receiver = event.node
		#self.log.info("WiFiCapabilities: uuid: {}, MAC: {}, capabilities: {}".format(receiver.uuid, event.macaddr, event.capabilities))
		self.mynodes[receiver.uuid] = {}
		self.mynodes[receiver.uuid]['MAC'] = event.macaddr
		self.mynodes[receiver.uuid]['capabilities'] = event.capabilities
		self.mynodes[receiver.uuid]['status'] = 'idle'
		self.mynodes[receiver.uuid]['details'] = ""
		self.mynodes[receiver.uuid]['config'] = {}
		capab_str = json.dumps(event.capabilities)
		device_data = (event.macaddr, receiver.uuid, capab_str)
		insert_query.insert_device_capabilities(device_data)
		self.setup_wifi_monitor(event.macaddr)

	def setup_wifi_ap(self, macaddr, ssid, power, channel, hw_mode, ht_capab):
		startap_event = WiFiConfigureAP(macaddr, ssid, power, channel, hw_mode, ht_capab)				
		self.send_event(startap_event)

	def setup_wifi_station(self, macaddr, ssid, ap, power, channel):
		startsta_event = WiFiConfigureStation(macaddr, ssid, ap, power, channel)				
		self.send_event(startsta_event)

	def setup_wifi_monitor(self, macaddr):
		startmon_event = WiFiConfigureMonitor(macaddr)				
		self.send_event(startmon_event)

	def stop_wifi(self, macaddr):
		stop_event = WiFiStopAll(macaddr)				
		self.send_event(stop_event)

	def find_node_by_mac(self, macaddr):
		for node in self.mynodes:
			if self.mynodes[node]['MAC'] == macaddr:
				return self.mynodes[node]
		return None

	@modules.on_event(WiFiLinkStatistics)
	def serve_linkstats_event(self, event):
		receiver = event.node
		txmac = event.txmac
		rxmac = event.rxmac
		rssi = event.rssi #in dBm
		tx_ret = event.tx_retries #in percents
		tx_fai = event.tx_failed #in percents
		tx_rate = event.tx_rate #in bps
		rx_rate = event.rx_rate #in bps
		tx_thr = event.tx_throughput #in bps
		rx_thr = event.rx_throughput #in bps
		tx_act = event.tx_activity #in percents
		rx_act = event.rx_activity #in percents

		link_data = (txmac, rxmac, rssi, tx_ret*100, tx_fai*100, tx_rate/1000000, rx_rate/1000000, tx_thr/1000000, rx_thr/1000000, tx_act*100, rx_act*100, datetime.now())
		insert_query.insert_link_statistics(link_data)

		#self.log.info("%s->%s link statistics:\n\tRSSI: %.0fdBm \n\ttx packet retries: %.2f%% \n\ttx packet fails: %.2f%% \n\ttx bitrate: %.2fMbps \n\trx bitrate: %.2fMbps \n\tachieved tx throughput: %.2fMbps \n\tachieved rx throughput: %.2fMbps \n\ttx activity: %.2f%% \n\trx activity: %.2f%%" % (txmac, rxmac, rssi, tx_ret*100, tx_fai*100, tx_rate/1000000, rx_rate/1000000, tx_thr/1000000, rx_thr/1000000, tx_act*100, rx_act*100))

	@modules.on_event(WiFiAPStatistics)
	def serve_apstats_event(self, event):
		receiver = event.node
		apmac = event.apmac
		stations = event.stations
		tot_ret = event.total_tx_retries #in percents
		tot_fai = event.total_tx_failed #in percents
		tot_tx_thr = event.total_tx_throughput #in bps
		tot_rx_thr = event.total_rx_throughput #in bps
		tot_tx_act = event.total_tx_activity #in percents
		tot_rx_act = event.total_rx_activity #in percents

		ap_data = (apmac, tot_ret*100, tot_fai*100, tot_tx_thr/1000000, tot_rx_thr/1000000, tot_tx_act*100, tot_rx_act*100, datetime.now())
		insert_query.insert_ap_statistics(ap_data)

		if receiver.uuid in self.mynodes:
			self.mynodes[receiver.uuid]['details'] = "connected to {} stations: {}".format(len(stations), stations)
			self.mynodes[receiver.uuid]['stations'] = stations	

		#self.log.info("AP (%s) statistics:\n\ttotal tx packet retries: %.2f%% \n\ttotal tx packet fails: %.2f%% \n\tachieved total tx throughput: %.2fMbps \n\tachieved total rx throughput: %.2fMbps \n\ttotal tx activity: %.2f%% \n\ttotal rx activity: %.2f%%" % (apmac, tot_tx_ret*100, tot_tx_fai*100, tot_tx_thr/1000000, tot_rx_thr/1000000, tot_tx_act*100, tot_rx_act*100))

	@modules.on_event(WiFiConfigureMonitorRsp)
	def serve_configure_monitor_rsp_event(self, event):
		receiver = event.node
		if receiver.uuid in self.mynodes:
			self.mynodes[receiver.uuid]['status'] = 'monitor'
			self.mynodes[receiver.uuid]['details'] = ""
			self.mynodes[receiver.uuid]['config'] = {}
			device_data = (event.macaddr, 1, None, None, None, None, None, None)
			insert_query.update_device_status(device_data)
		
	@modules.on_event(WiFiConfigureStationRsp)
	def serve_configure_station_rsp_event(self, event):
		receiver = event.node
		apmac = event.apmac
		staconf = event.sta_config
		if receiver.uuid in self.mynodes:
			self.mynodes[receiver.uuid]['status'] = 'station'
			self.mynodes[receiver.uuid]['details'] = "connected to BSSID: {}".format(apmac)
			self.mynodes[receiver.uuid]['config'] = staconf
			device_data = (event.macaddr, 3, None, staconf['power'], staconf['ssid'], staconf['channel'], None, apmac)
			insert_query.update_device_status(device_data)
			
	@modules.on_event(WiFiConfigureAPRsp)
	def serve_apconnection_rsp_event(self, event):
		receiver = event.node
		apconf = event.ap_config
		if receiver.uuid in self.mynodes:
			self.mynodes[receiver.uuid]['status'] = 'AP'
			self.mynodes[receiver.uuid]['config'] = apconf
			device_data = (event.macaddr, 2, apconf['hw_mode'], apconf['power'], apconf['ssid'], apconf['channel'], None, None)
			if 'stations' in self.mynodes[receiver.uuid]:
				stations = self.mynodes[receiver.uuid]['stations']
				for staind in range(0, len(stations)-1):
					stamac = stations[staind]
					if self.find_node_by_mac(stamac) is not None:
						ssid = apconf['ssid']
						power = apconf['power']
						channel = apconf['channel']
						apmac = self.mynodes[receiver.uuid]['MAC']
						self.setup_wifi_station(stamac, ssid, apmac, power, channel)

			insert_query.update_device_status(device_data)

	@modules.on_event(RRMRegister)
	def serve_rrm_register_event(self, event):
		#print("RRMRegister")
		receiver = event.node
		self.myrrm_uuid = receiver.uuid

	@modules.on_event(RRMReconfigureAP)
	def serve_rrm_reconfigure_ap_event(self, event):
		self.setup_wifi_ap(event.macaddr, event.ssid, event.power, event.channel, event.hw_mode, event.ht_capab)
