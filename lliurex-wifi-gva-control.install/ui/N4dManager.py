#!/usr/bin/python3

import n4d.client
import os
import sys
import syslog
import json
import codecs
import pwd
import grp

class N4dManager:

	APPLY_CHANGES_SUCCESSFUL=10
	CHANGE_WIFI_ERROR=-10
	CHANGE_AUTOLOGIN_PASSWORD_ERROR=-20
	CHANGE_AUTOLOGIN_STATUS_ERROR=-30
	CHANGE_MULTIPLE_ERROR=-40
	ERROR_PASSWORDS_NOT_MATCH=-50
	ERROR_PASSWORD_EMPTY=-60
	ERROR_LOADING_CONFIGURATION=-70

	def __init__(self):

		self.debug=True
		self.isWifiEnabled=False
		self.currentWifiOption=2
		self.currentPassword=""
		self.wifiConfiguration=0
		
	#def __init__

	def setServer(self,ticket):
		
		ticket=ticket.replace('##U+0020##',' ')
		self.currentUser=ticket.split(' ')[2]
		tk=n4d.client.Ticket(ticket)
		self.client=n4d.client.Client(ticket=tk)

		self.writeLog("Init session in lliurex-wifi-control GUI")
		self.writeLog("User login in GUI: %s"%self.currentUser)
	
	#def setServer

	def loadConfig(self,step="Initial"):

		'''
			Values:
				- 0: Disable
				- 1: WIFI_PROF
				- 2: WIFI_ALU
				- 3: WIFI_ALU+AUTOLOGIN
		'''

		try:
			self.writeLog("Wifi Control. %s configuration:"%step)
			self.wifiConfiguration=self.client.EscolesConectades.get_settings()
			wifiPassword=self.client.EscolesConectades.get_autologin()
			
			if self.wifiConfiguration in [0,1,2,3]:
				if self.wifiConfiguration==0:
					self.isWifiEnabled=False
				else:
					self.isWifiEnabled=True
					self.currentWifiOption=self.wifiConfiguration

			if wifiPassword!=None:
				self.currentPassword=wifiPassword

			self.writeLog("- Current Wifi Option: %s"%(self.wifiConfiguration))

			return True

		except Exception as e:
			self.writeLog("- Error loading configuration: %s"%(str(e)))
			return False

	#def loadConfig

	def applyChanges(self,info):

		changePassword=False
		enableAutologin=False
		errorCount=0
		currentPassword=info[2]

		if info[0]:
			currentWifiOption=info[1]
			if currentWifiOption!=self.currentWifiOption:
				if currentWifiOption==3:
					enableAutologin=True
			if currentWifiOption==3:
				if currentPassword!=self.currentPassword:
					changePassword=True
					enableAutologin=True		
		else:
			currentWifiOption=0

		if currentWifiOption!=self.wifiConfiguration:
			self.writeLog("Changes in wifi configuration:")
			self.writeLog("- Action: Changed Wifi Option to: %s"%(str(currentWifiOption)))
			try:
				ret=self.client.EscolesConectades.set_settings(currentWifiOption)
				self.writeLog("- Result: Changes apply successful")
			except Exception as e:
				self.writeLog("- Result: Error applying changes: %s"%str(e))
				result=[False,N4dManager.CHANGE_WIFI_ERROR]
				errorCount+=1

		if changePassword:
			self.writeLog("Changes in autologin password:")
			self.writeLog("- Action: Update password")
			try:
				ret=self.client.EscolesConectades.set_autologin(currentPassword)
				self.writeLog("- Result: changes apply successful")
			except Exception as e:
				self.writeLog("- Result: Error applying changes: %s"%str(e))
				result=[False,N4dManager.CHANGE_AUTOLOGIN_PASSWORD_ERROR]
				errorCount+=1

		if enableAutologin:
			self.writeLog("Changes in Autologin")
			if currentWifiOption==3:
				self.writeLog("- Action: Enable autologin")
				enable=True
			else:
				self.writeLog("- Action: Disable autologin")
				enable=False

			try:
				#ret: llamada a plugin para activar autologin
				self.writeLog("- Result: Changes apply successful")
			except Exception as e:
				self.writeLog("- Result: Error applying changes: %s"%str(e))
				result=[False,N4dManager.CHANGE_AUTOLOGIN_STATUS_ERROR]
				errorCount+=1

		if errorCount==0:
			self.loadConfig("End")
			result=[True,N4dManager.APPLY_CHANGES_SUCCESSFUL]
		else:
			if errorCount>1:
				result=[False,N4dManager.CHANGE_MULTIPLE_ERROR]

		return result

	#def applyChanges

	def writeLog(self,msg):

		syslog.openlog("WIFI-GVA-CONTROL")
		syslog.syslog(msg)

	#def writeLog

#class N4dManager
