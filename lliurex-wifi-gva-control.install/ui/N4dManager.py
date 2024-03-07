#!/usr/bin/python3

import n4d.client
import os
import subprocess
import sys
import syslog
import json
import codecs
import pwd
import grp

class N4dManager:

	APPLY_CHANGES_SUCCESSFUL=10
	WARNING_CDC_ACTIVATION_REQUIRED=20
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
		self.currentAutologinStatus=False
		
	#def __init__

	def setServer(self,ticket):
		
		ticket=ticket.replace('##U+0020##',' ')
		self.currentUser=ticket.split(' ')[2]
		tk=n4d.client.Ticket(ticket)
		self.client=n4d.client.Client(ticket=tk)

		self.writeLog("Init session in lliurex-wifi-gva-control GUI")
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
			self.wifiConfiguration=self.client.WifiEduGva.get_settings()
			wifiPassword=self.client.WifiEduGva.get_autologin()
			self.currentAutologinStatus=self._checkIfAutologinIsEnabled()

			if self.wifiConfiguration in [0,1,2,3]:
				if self.wifiConfiguration==0:
					self.isWifiEnabled=False
					self.currentWifiOption=2
				else:
					self.isWifiEnabled=True
					self.currentWifiOption=self.wifiConfiguration

			if wifiPassword!=None:
				self.currentPassword=wifiPassword

			self.writeLog("- Current Wifi Option: %s"%(self.wifiConfiguration))
			self.writeLog("- Autologin: %s"%(str(self.currentAutologinStatus)))
			
			return True

		except Exception as e:
			self.writeLog("- Error loading configuration: %s"%(str(e)))
			return False

	#def loadConfig

	def applyChanges(self,info):

		'''
			Actions in autologin:
				- -1: Nothing
				- 0: Enabled
				- 1: Disabled
				- 2: Updated Password
		'''

		changeWifi=False
		changePassword=False
		actionAutologin=-1
		errorCount=0
		currentPassword=info[2]

		if info[0]:
			currentWifiOption=info[1]
		else:
			currentWifiOption=0

		if currentWifiOption!=self.wifiConfiguration:
			changeWifi=True
			if currentWifiOption==3:
				actionAutologin=0
			else:
				if self.currentAutologinStatus:
					actionAutologin=1
		
		if currentPassword!=self.currentPassword:
			changePassword=True
			if currentWifiOption==3:
				if actionAutologin==-1:
					if self.currentAutologinStatus:
						actionAutologin=2
					else:
						actionAutologin=0		

		if changeWifi:
			self.writeLog("Changes in wifi configuration:")
			self.writeLog("- Action: Changed Wifi Option to: %s"%(str(currentWifiOption)))
			try:
				ret=self.client.WifiEduGva.set_settings(currentWifiOption)
				self.writeLog("- Result: Changes apply successful")
			except Exception as e:
				self.writeLog("- Result: Error applying changes: %s"%str(e))
				result=[False,N4dManager.CHANGE_WIFI_ERROR]
				errorCount+=1

		if changePassword:
			self.writeLog("Changes in autologin password:")
			if currentPassword!="":
				self.writeLog("- Action: Update password")
			else:
				self.writeLog("- Action: Clear password")
			try:
				ret=self.client.WifiEduGva.set_autologin(currentPassword)
				self.writeLog("- Result: changes apply successful")
			except Exception as e:
				self.writeLog("- Result: Error applying changes: %s"%str(e))
				result=[False,N4dManager.CHANGE_AUTOLOGIN_PASSWORD_ERROR]
				errorCount+=1


		if actionAutologin!=-1:
			self.writeLog("Changes in autologin")
			try:
				if actionAutologin==0:
					self.writeLog("- Action: Enable autologin")
					ret=self.client.AlumnatAccountManager.enable_alumnat_user()
				elif actionAutologin==1:
					self.writeLog("- Action: Disable autologin")
					ret=self.client.AlumnatAccountManager.disable_alumnat_user()
				elif actionAutologin==2:
					self.writeLog("- Action: Updated password")
					ret=self.client.AlumnatAccountManager.fix_alumnat_password()
				
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

	def _checkIfAutologinIsEnabled(self):

		try:
			ret=self.client.AlumnatAccountManager.get_alumnat_status()['status']
		except:
			ret=False

		return ret

	#def __checkIfAutologinIsEnabled

	def writeLog(self,msg):

		syslog.openlog("WIFI-GVA-CONTROL")
		syslog.syslog(msg)

	#def writeLog

	def getIntegrationCDCStatus(self):

		cmd="cdccli -t"
		p=subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
		poutput=p.communicate()
		rc=p.returncode
		
		if rc==0:
			return True
		else:
			return False

	#def getIntegrationCDCStatus

#class N4dManager
