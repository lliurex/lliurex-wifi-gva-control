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

	KIRIGAMI_MSG_OK=0
	KIRIGAMI_MSG_ERROR=1
	KIRIGAMI_MSG_WARNING=2
	KIRIGAMI_MSG_INFO=3


	def __init__(self):

		self.debug=True
		self.isWifiEnabled=False
		self.currentWifiOption=1
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
		self.writeLog(f"User login in GUI: {self.currentUser}")
	
	#def setServer

	def loadConfig(self,step="Initial"):

		'''
			Values:
				- 0: Disable
				- 1: WIFI_EDU
				- 2: WIFI_EDU:for backward compatibility 
				- 3: WIFI_EDU+AUTOLOGIN
		'''

		try:
			self.writeLog(f"Wifi Control. {step} configuration:")
			self.wifiConfiguration=self.client.WifiEduGva.get_settings()
			wifiPassword=self.client.WifiEduGva.get_autologin()
			self.currentAutologinStatus=self._checkIfAutologinIsEnabled()
		except Exception as e:
			self.writeLog(f"- Error loading configuration: {e}")
			return {"status":False,"code":N4dManager.ERROR_LOADING_CONFIGURATION,"type":N4dManager.KIRIGAMI_MSG_ERROR}

		if self.wifiConfiguration in [0,1,2,3]:
			if self.wifiConfiguration==0:
				self.isWifiEnabled=False
				self.currentWifiOption=1
			else:
				self.isWifiEnabled=True
				self.currentWifiOption=self.wifiConfiguration

		if wifiPassword is not None:
			self.currentPassword=wifiPassword

		self.currentWifiSettings={
			"isWifiEnabled":self.isWifiEnabled,
			"currentWifiOption":self.currentWifiOption,
			"currentPassword":wifiPassword if wifiPassword is not None else "",
			"confirmPassword":""
		}

		self.writeLog(f"- Current Wifi Option: {self.wifiConfiguration}")
		self.writeLog(f"- Autologin: {self.currentAutologinStatus}")
			
		return {"status":True,"code":"","type":""}

	#def loadConfig

	def applyChanges(self, info):
	    '''
	    Actions in autologin:
	        - -1: Nothing
	        -  0: Enabled
	        -  1: Disabled
	        -  2: Updated Password
	    '''
	    changeWifi = False
	    changePassword = False
	    lastError = None
	    actionAutologin = -1
	    errorCount = 0

	    currentPassword = info.get('currentPassword')
	    confirmPassword = info.get("confirmPassword")
	    currentWifiOption = info.get('currentWifiOption') if info.get('isWifiEnabled') else 0

	    if currentWifiOption == 3:
	        if not currentPassword:
	            return {"status": False, "code": N4dManager.ERROR_PASSWORD_EMPTY, "type": N4dManager.KIRIGAMI_MSG_ERROR}
	        if (currentPassword != self.currentPassword) and (currentPassword != confirmPassword):
	            return {"status": False, "code": N4dManager.ERROR_PASSWORDS_NOT_MATCH, "type": N4dManager.KIRIGAMI_MSG_ERROR}

	    if currentWifiOption != self.wifiConfiguration:
	        changeWifi = True
	        if currentWifiOption == 3:
	            actionAutologin = 0
	        elif self.currentAutologinStatus:
	            actionAutologin = 1

	    if currentPassword != self.currentPassword:
	        changePassword = True
	        if currentWifiOption == 3 and actionAutologin == -1:
	            actionAutologin = 2 if self.currentAutologinStatus else 0

	    if changeWifi:
	        self.writeLog("Changes in wifi configuration:")
	        self.writeLog(f"- Action: Changed Wifi Option to: {currentWifiOption}")
	        try:
	            self.client.WifiEduGva.set_settings(currentWifiOption)
	            self.writeLog("- Result: Changes apply successful")
	        except Exception as e:
	            self.writeLog(f"- Result: Error applying changes: {e}")
	            lastError = N4dManager.CHANGE_WIFI_ERROR
	            errorCount += 1

	    if changePassword:
	        self.writeLog("Changes in autologin password:")
	        action_text = "Update password" if currentPassword else "Clear password"
	        self.writeLog(f"- Action: {action_text}")
	        try:
	            self.client.WifiEduGva.set_autologin(currentPassword)
	            self.writeLog("- Result: changes apply successful")
	        except Exception as e:
	            self.writeLog(f"- Result: Error applying changes: {e}")
	            lastError = N4dManager.CHANGE_AUTOLOGIN_PASSWORD_ERROR
	            errorCount += 1

	    if actionAutologin != -1:
	        self.writeLog("Changes in autologin")
	        try:
	            if actionAutologin == 0:
	                self.writeLog("- Action: Enable autologin")
	                self.client.AlumnatAccountManager.enable_alumnat_user()
	            elif actionAutologin == 1:
	                self.writeLog("- Action: Disable autologin")
	                self.client.AlumnatAccountManager.disable_alumnat_user()
	            elif actionAutologin == 2:
	                self.writeLog("- Action: Updated password")
	                self.client.AlumnatAccountManager.fix_alumnat_password()

	            self.writeLog("- Result: Changes apply successful")
	        except Exception as e:
	            self.writeLog(f"- Result: Error applying changes: {e}")
	            lastError = N4dManager.CHANGE_AUTOLOGIN_STATUS_ERROR
	            errorCount += 1

	    if errorCount > 1:
	        return {"status": False, "code": N4dManager.CHANGE_MULTIPLE_ERROR, "type": N4dManager.KIRIGAMI_MSG_ERROR}
	    if errorCount == 1:
	        return {"status": False, "code": lastError, "type": N4dManager.KIRIGAMI_MSG_ERROR}

	    self.loadConfig("End")
	    
	    return {"status": True, "code": N4dManager.APPLY_CHANGES_SUCCESSFUL, "type": N4dManager.KIRIGAMI_MSG_OK}

	#def applyChanges

	def _checkIfAutologinIsEnabled(self):

		try:
			return self.client.AlumnatAccountManager.get_alumnat_status().get('status',False)
		except Exception:
			return False

	#def _checkIfAutologinIsEnabled

	def writeLog(self,msg):

		syslog.openlog("WIFI-GVA-CONTROL")
		syslog.syslog(msg)

	#def writeLog

	def getIntegrationCDCStatus(self):

		try:
			return subprocess.call(["cdccli", "-t"], stdout=subprocess.DEVNULL) == 0
		except Exception:
			return False

	#def getIntegrationCDCStatus

#class N4dManager
