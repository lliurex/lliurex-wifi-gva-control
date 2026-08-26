#!/usr/bin/env python3

from enum import IntEnum

import os
import subprocess
import n4d.client
import sys
import syslog
import pwd
import grp
import getpass
import signal
import codecs

signal.signal(signal.SIGINT,signal.SIG_IGN)

class WifiGvaControlCliManager(object):

	class WifiMode(IntEnum):
		
		DISABLE=0
		ENABLE=1
		LEGACY=2
		AUTOLOGIN=3
		EASYLOGIN=4

	#class WifiMode

	def __init__(self,mode):
		
		self.isWifiConnectionEnabled=False
		self.currentWifiConnection=-1
		self.isAlumnatPasswordConfigured=False
		self.currentAlumnatPassword=None
		self.isCDCIntegrationEnabled=False
		self.currentUser=""
		self.unattendedMode=mode
		self.n4dClient=n4d.client.Client()
		self._getCurrentUser()
		self._getInfo("Initial")

	#def __init__

	def showCurrentConfig(self):

		self._writeLog("- Action: get current configuration")
		self._createClient()

		print('   [Wifi-GVA-Control]: Current configuration')
		print(f'      - Wifi Connection Enabled: {self.isWifiConnectionEnabled}')
		if self.isWifiConnectionEnabled:
			defaultConnection=self._mappingWifiOption(self.currentWifiConnection,"IntToText")
			print(f'      - Default option for Wifi Connection: {defaultConnection}')
		print(f'      - Password for alumnat user configured: {self.isAlumnatPasswordConfigured}')

		if self.isWifiConnectionEnabled and self.currentWifiConnection not in (WifiGvaControlCliManager.WifiMode.AUTOLOGIN,WifiGvaControlCliManager.WifiMode.EASYLOGIN):
			if not self.isCDCIntegrationEnabled:
				print('   [Wifi-GVA-Control]: WARNING It is necessary to activate the integration with ID to be able to log in with WIFI GVA')

		return 0
	
	#def showCurrentConfig

	def showAlumnatPassword(self):

		self._writeLog("- Action: get current password for alumnat user")
		self._createClient()

		if self.currentAlumnatPassword is not None:
			print(f'   [Wifi-GVA-Control]: Current password for alumnat user: {self.currentAlumnatPassword}')
		else:
			print('   [Wifi-GVA-Control]: Password for alumnat user not configured')
	
		return 0

	#def showAlumnatPassword

	def enableWifi(self,wifiOption,password=None,confirmPassword=None):

		wifiValue=self._mappingWifiOption(wifiOption,"TextToInt")
		forcePasswordUpdate=False

		if wifiValue==-1:
			print('   [Wifi-GVA-Control]: The option indicated for Wifi is not valid')
			return 0

		if wifiValue==self.currentWifiConnection:
			print('   [Wifi-GVA-Control]: Wifi connection with the indicated option already configured. Nothing to do')
			return 0
		
		if wifiValue in (WifiGvaControlCliManager.WifiMode.AUTOLOGIN,WifiGvaControlCliManager.WifiMode.EASYLOGIN): 
			if not self.isAlumnatPasswordConfigured:
				if not self._checkPassword(password,confirmPassword):
					return 0
			else:
				if password and password!=self.currentAlumnatPassword:
					if not self._checkPassword(password,confirmPassword):
						return 0
					forcePasswordUpdate=True
		
		if not self.unattendedMode:
			response=input('   [Wifi-GVA-Control]: Do you want to activate the automatic connection to the indicated Wifi? (yes/no)): ').lower()
		else:
			response='yes'

		if not response.startswith('y'):
			print('   [Wifi-GVA-Control]: Action canceled')
			return 0

		try:
			self._writeLog("Changes in configuration of Wifi GVA:")
			self._writeLog(f"- Action: activate Wifi connection with option: {wifiValue}")
			self._createClient()
			ret=self.n4dClient.WifiEduGva.set_settings(int(wifiValue))
			self._writeLog("- Result: Changes apply successful")

			if wifiValue not in (WifiGvaControlCliManager.WifiMode.AUTOLOGIN,WifiGvaControlCliManager.WifiMode.EASYLOGIN):
				if self.isAutologinConfigured:
					self._writeLog("- Action: disable autologin")
					ret=self.n4dClient.AlumnatAccountManager.disable_alumnat_user()
					self._writeLog("- Result: Changes apply successful")
			else:
				if not self.isAlumnatPasswordConfigured or forcePasswordUpdate:
					self._writeLog("- Action: set password for alumnat user")
					ret=self.n4dClient.WifiEduGva.set_autologin(password)
					self._writeLog("- Result: Changes apply successful")

				if not self.isAutologinConfigured:
					self._writeLog("- Action: enable autologin")
					ret=self.n4dClient.AlumnatAccountManager.enable_alumnat_user()
					self._writeLog("- Result: Changes apply successful")
				
			print('   [Wifi-GVA-Control]: Action completed successfull')
			self._getInfo("End")
			
			if wifiValue not in (WifiGvaControlCliManager.WifiMode.AUTOLOGIN,WifiGvaControlCliManager.WifiMode.EASYLOGIN) and not self.isCDCIntegrationEnabled:
				print('   [Wifi-GVA-Control]: WARNING It is necessary to activate the integration with ID to be able to log in with WIFI GVA')
			return 0

		except n4d.client.CallFailedError as e:
			self._writeLog(f"- Error applying changes: {e.code}")
			print(f'   [Wifi-GVA-Control]: Error. Unable to enable Wifi connection')
			return 1
					
	#def enableWifi

	def disableWifi(self):

		if not self.isWifiConnectionEnabled:
			print('   [Wifi-GVA-Control]: Wifi connection already disabled. Nothing to do')
			return 0
	
		if not self.unattendedMode:
			response=input('   [Wifi-GVA-Control]: Do you want to disable the automatic connection to the Wifi? (yes/no)): ').lower()
		else:
			response='yes'

		if not response.startswith('y'):
			print('   [Wifi-GVA-Control]: Action canceled')
			return 0
		
		try:
			self._writeLog("Changes in configuration of Wifi GVA:")
			self._writeLog("- Action: disable Wifi connection")
			self._createClient()
			ret=self.n4dClient.WifiEduGva.set_settings(0)
			self._writeLog("- Result: Changes apply successful")

			if self.isAutologinConfigured:
				self._writeLog("- Action: disable autologin")
				ret=self.n4dClient.AlumnatAccountManager.disable_alumnat_user()
				self._writeLog("- Result: Changes apply successful")

			print('   [Wifi-GVA-Control]: Action completed successfull')
			self._getInfo("End")
			return 0

		except n4d.client.CallFailedError as e:
			self._writeLog(f"- Error applying changes: {e.code}")
			print('   [Wifi-GVA-Control]: Error. Unable to disable Wifi connection')
			return 1

	#def disableWifi

	def updateAlumnatPassword(self,password,confirmPassword):

		if not self._checkPassword(password,confirmPassword):
			return 0
		
		if password==self.currentAlumnatPassword:
			print('   [Wifi-GVA-Control]: Password of alumnat user already exists. Nothing to do')
			return 0

		if not self.unattendedMode:
			response=input('   [Wifi-GVA-Control]: Do you want to update the password of the alumnat user? (yes/no)): ').lower()
		else:
			response='yes'
			
		if not response.startswith('y'):
			print('   [Wifi-GVA-Control]: Action canceled')
			return 0
		
		try:
			self._writeLog("Changes in configuration of Wifi GVA:")
			self._writeLog('- Action: update alumnat password')
			self._createClient()
			ret=self.n4dClient.WifiEduGva.set_autologin(password)
			self._writeLog("- Result: changes apply successful")
			print('   [Wifi-GVA-Control]: Action completed successfull')
			return 0

		except n4d.client.CallFailedError as e:
			self._writeLog(f"- Error applying changes: {e.code}")
			print('   [Wifi-GVA-Control]: Error. Unable to update password of alumnat user')
			return 1
	
	#def updateAlumnatPassword

	def removeAlumnatPassword(self):

		if not self.isAlumnatPasswordConfigured:
			print('   [Wifi-GVA-Control]: Password for alumnat user already removed. Nothing to do')
			return 0

		if self.currentWifiConnection in (WifiGvaControlCliManager.WifiMode.AUTOLOGIN,WifiGvaControlCliManager.WifiMode.EASYLOGIN):
			print('   [Wifi-GVA-Control]: Password for alumnat user cannot be deleted because the AUTOLOGIN or EASYLOGIN option is activated')
			return 0
		
		if not self.unattendedMode:
			response=input('   [Wifi-GVA-Control]: Do you want to remove the password of alumnat user? (yes/no)): ').lower()
		else:
			response='yes'

		if not response.startswith('y'):
			print('   [Wifi-GVA-Control]: Action canceled')
			return 0
			
		try:
			self._writeLog("Changes in configuration of Wifi GVA:")
			self._writeLog('- Action: remove alumnat password')
			self._createClient()
			ret=self.n4dClient.WifiEduGva.set_autologin("")
			self._writeLog("- Result: changes apply successful")
			print('   [Wifi-GVA-Control]: Action completed successfull')
			self._getInfo("End")
			return 0

		except n4d.client.CallFailedError as e:
			self._writeLog(f"- Error applying changes: {e.code}"%e.code)
			print('   [Wifi-GVA-Control]: Error. Unable to remove password of alumnat user')
			return 1

	#de removeAlumnatPassword

	def n4dUpdatePassword(self,password):

		if self.currentUser!="":
			print('   [Wifi-GVA-Control]: Option valid only for schedled password changes')
			return 0
		if not self.isAlumnatPasswordConfigured:
			return 0
		
		try:
			self._writeLog("Changes in configuration of Wifi GVA:")
			self._writeLog('- Action: update alumnat password (with n4d one-shot)')
			self._createClient()
			tmpPassword=codecs.decode(password,'rot13')
			ret=self.n4dClient.WifiEduGva.set_autologin(tmpPassword)
			self._writeLog("- Result: changes apply successful")
			print('   [Wifi-GVA-Control]: Action completed successfull')
			self._getInfo("End")
			return 0

		except n4d.client.CallFailedError as e:
			self._writeLog(f"- Error applying changes: {e.code}")
			print('   [Wifi-GVA-Control]: Error. Unable to update password of alumnat user')
			return 1

	#def n4dUpdatePassword

	def _createClient(self):

		if self.currentUser!="":
			password=getpass.getpass('   [Wifi-GVA-Control]: Enter your password:')
			client=n4d.client.Client("https://localhost:9779",self.currentUser,password)
			
			try:
				ticket=client.get_ticket()
				self.n4dClient=n4d.client.Client(ticket=ticket)
			except Exception as e:
				msg="Authentication failed. Unable to execute action"
				self._writeLog(msg)
				print(f"   [Wifi-GVA-Control]: {msg}")
				sys.exit(1)
		else:
			masterKey=n4d.client.Key.master_key()
			
			if masterKey.valid():
				self.n4dClient=n4d.client.Client(key=masterKey)
			else:
				print('   [Wifi-GVA-Control]: You need root privilege to run this tool')

	#def _createClient

	def _getInfo(self,step="Initial"):

		try:
			self._writeLog(f"Wifi Control. {step} configuration")
			wifiConfiguration=self.n4dClient.WifiEduGva.get_settings()
			wifiPassword=self.n4dClient.WifiEduGva.get_autologin()
			self.isAutologinConfigured=self._checkIfAutologinIsEnabled()

			if wifiConfiguration in WifiGvaControlCliManager.WifiMode.__members__.values():
				if wifiConfiguration==WifiGvaControlCliManager.WifiMode.DISABLE:
					self.isWifiConnectionEnabled=False
					self.currentWifiConnection=-1
				else:
					self.isWifiConnectionEnabled=True
					self.currentWifiConnection=wifiConfiguration

			if not wifiPassword:
				self.isAlumnatPasswordConfigured=False
			else:
				self.isAlumnatPasswordConfigured=True
				self.currentAlumnatPassword=wifiPassword

			self.isCDCIntegrationEnabled=self._getIntegrationCDCStatus()

			self._writeLog(f"- Current Wifi Option: {wifiConfiguration}")
			self._writeLog(f"- Password for alumnat user configured: {self.isAlumnatPasswordConfigured}")
			
			return True

		except Exception as e:
			self._writeLog(f"- Error loading configuration: {e}")
			return False

	#def _getInfo

	def _mappingWifiOption(self,wifiOption,mappingType):

		if mappingType=="TextToInt":
			mapping ={
				"WIFI_EDU":WifiGvaControlCliManager.WifiMode.ENABLE,
				"ALUMNAT": WifiGvaControlCliManager.WifiMode.AUTOLOGIN,
				"EASY_LOGIN": WifiGvaControlCliManager.WifiMode.EASYLOGIN
			}
			return mapping.get(wifiOption,-1)
		else:
			mapping={
				WifiGvaControlCliManager.WifiMode.ENABLE:"WIFI_EDU",
				WifiGvaControlCliManager.WifiMode.LEGACY:"WIFI_EDU",
				WifiGvaControlCliManager.WifiMode.AUTOLOGIN:"ALUMNAT",
				WifiGvaControlCliManager.WifiMode.EASYLOGIN:"EASY_LOGIN"
			}
			return mapping.get(wifiOption,"UNKNOWN")

	#def _mappingWifiOption

	def _checkIfAutologinIsEnabled(self):

		try:
			ret=self.n4dClient.AlumnatAccountManager.get_alumnat_status()['status']
		except:
			ret=False

		return ret

	#def _checkIfAutologinIsEnabled

	def _checkPassword(self,password,confirmPassword):

		if not password:
			print('   [Wifi-GVA-Control]: No password has been indicated for the alumnat user')
			return False
		
		if password!=confirmPassword:
			print('   [Wifi-GVA-Control]: The given passwords for the alumnat user do not match')
			return False

		return True

	#def _checkPassword

	def _getCurrentUser(self):

		sudoUser=os.environ.get("SUDO_USER","")
		loginUser=""
		pkexecUser=""

		
		try:
			loginUser=os.getlogin()
		except:
			pass

		pkexec_uid=os.environ.get("PKEXEC_UID")
		if pkexec_uid:
			try:
				pkexecUser=subprocess.check_output(["id", "-un", pkexec_uid]).decode().strip()
			except:
				pass

		if pkexecUser and pkexecUser !="root":
			self.currentUser=pkexecUser

		elif sudoUser and sudoUser!="root":
			self.currentUser=sudoUser
			
		else:
			self.currentUser=loginUser

		self._writeLog("Init session in lliurex-wifi-gva-control CLI")
		if loginUser:
			self._writeLog(f"User login in CLI: {self.currentUser}")
		else:
			self._writeLog("User login in CLI: No current user detected. A script may have been executed at login")

		if self.unattendedMode:
			self.currentUser=""
			
		self._writeLog(f"Unattended Mode:{self.unattendedMode}")

	#def _getCurrentUser

	def _getIntegrationCDCStatus(self):

		try:
			result=subprocess.run(["cdccli","-t"],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
			return result.returncode==0
		except FileNotFoundError:
			return False

	#def _getIntegrationCDCStatus

	def _writeLog(self,msg):

		syslog.openlog("WIFI-GVA-CONTROL")
		syslog.syslog(msg)

	#def _writeLog

#class WifiGvaControlCliManager	



