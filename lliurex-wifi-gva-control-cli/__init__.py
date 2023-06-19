#!/usr/bin/env python3

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

	def __init__(self,mode):
		
		self.isWifiConnectionEnabled=False
		self.currentWifiConnection=2
		self.isAlumnatPasswordConfigured=False
		self.currentAlumnatPassword=None
		self.currentUser=""
		self.unattendedMode=mode
		self.n4dClient=n4d.client.Client()
		self._getCurrentUser()
		self._getInfo("Initial")

	#def __init__


	def createClient(self):

		if self.currentUser!="":
			password=getpass.getpass('   [Wifi-GVA-Control]: Enter your password:')
			client=n4d.client.Client("https://localhost:9779",self.currentUser,password)
			
			try:
				ticket=client.get_ticket()
				self.n4dClient=n4d.client.Client(ticket=ticket)
			except Exception as e:
				msg="Authentication failed. Unable to execute action"
				self.writeLog(msg)
				print("   [Wifi-GVA-Control]: %s"%msg)
				sys.exit(1)
		else:
			masterKey=n4d.client.Key.master_key()
			
			if masterKey.valid():
				self.n4dClient=n4d.client.Client(key=masterKey)
			else:
				print('   [Wifi-GVA-Control]: You need root privilege to run this tool')

	#def createClient

	def showCurrentConfig(self):

		self.writeLog("- Action: get current configuration")
		self.createClient()

		print('   [Wifi-GVA-Control]: Current configuration')
		print('      - Wifi Connection Enabled: %s'%(str(self.isWifiConnectionEnabled)))
		if self.isWifiConnectionEnabled:
			defaultConnection=self._mappingWifiOption(self.currentWifiConnection,"IntToText")
			print('      - Default option for Wifi Connection: %s'%(defaultConnection))
		print('      - Password for alumnat user configured: %s'%str(self.isAlumnatPasswordConfigured))

		return 0
	
	#def showCurrentConfig

	def showAlumnatPassword(self):

		self.writeLog("- Action: get current password for alumnat user")
		self.createClient()

		if self.currentAlumnatPassword!=None:
			print('   [Wifi-GVA-Control]: Current password for alumnat user: %s'%self.currentAlumnatPassword)
		else:
			print('   [Wifi-GVA-Control]: Password for alumnat user not configured')
	
		return 0

	#def showAlumnatPassword

	def enableWifi(self,wifiOption,password=None,confirmPassword=None):

		wifiValue=self._mappingWifiOption(wifiOption,"TextToInt")

		if wifiValue==-1:
			print('   [Wifi-GVA-Control]: The option indicated for Wifi is not valid')
			return 0
		else: 
			if wifiValue!=self.currentWifiConnection:
				if wifiValue==3 and not self.isAlumnatPasswordConfigured:
					if self._checkPassword(password,confirmPassword):
						return 0
				
				if not self.unattendedMode:
					response=input('   [Wifi-GVA-Control]: Do you want to activate the automatic connection to the indicated Wifi? (yes/no)): ').lower()
				else:
					response='yes'

				if response.startswith('y'):
					try:
						self.writeLog("Changes in configuration of Wifi GVA:")
						self.writeLog("- Action: activate Wifi connection with option: %s"%wifiValue)
						self.createClient()
						ret=self.n4dClient.WifiEduGva.set_settings(wifiValue)
						self.writeLog("- Result: Changes apply successful")

						if wifiValue!=3:
							if self.isAutologinConfigured:
								self.writeLog("- Action: disable autologin")
								ret=self.n4dClient.AlumnatAccountManager.disable_alumnat_user()
								self.writeLog("- Result: Changes apply successful")
						else:
							if not self.isAlumnatPasswordConfigured:
								self.writeLog("- Action: set password for alumnat user")
								ret=self.n4dClient.WifiEduGva.set_autologin(password)
								self.writeLog("- Result: Changes apply successful")

							if not self.isAutologinConfigured:
								self.writeLog("- Action: enable autologin")
								ret=self.n4dClient.AlumnatAccountManager.enable_alumnat_user()
								self.writeLog("- Result: Changes apply successful")
							
						print('   [Wifi-GVA-Control]: Action completed successfull')
						self._getInfo("End")
						return 0

					except n4d.client.CallFailedError as e:
						self.writeLog("- Error applying changes: %s"%e.code)
						print('   [Wifi-GVA-Control]: Error. Unable to enable Wifi connection')
						return 1
				else:
					print('   [Wifi-GVA-Control]: Action canceled')
					return 0
			else:
				print('   [Wifi-GVA-Control]: Wifi connection with the indicated option already configured. Nothing to do')
				return 0
					
	#def enableWifi

	def disableWifi(self):

		if self.isWifiConnectionEnabled:
			if not self.unattendedMode:
				response=input('   [Wifi-GVA-Control]: Do you want to disable the automatic connection to the Wifi? (yes/no)): ').lower()
			else:
				response='yes'

			if response.startswith('y'):
				try:
					self.writeLog("Changes in configuration of Wifi GVA:")
					self.writeLog("- Action: disable Wifi connection")
					self.createClient()
					ret=self.n4dClient.WifiEduGva.set_settings(0)
					self.writeLog("- Result: Changes apply successful")
	
					if self.isAutologinConfigured:
						self.writeLog("- Action: disable autologin")
						ret=self.n4dClient.AlumnatAccountManager.disable_alumnat_user()
						self.writeLog("- Result: Changes apply successful")

					print('   [Wifi-GVA-Control]: Action completed successfull')
					self._getInfo("End")
					return 0

				except n4d.client.CallFailedError as e:
					self.writeLog("- Error applying changes: %s"%e.code)
					print('   [Wifi-GVA-Control]: Error. Unable to disable Wifi connection')
					return 1
			else:
				print('   [Wifi-GVA-Control]: Action canceled')
				return 0	
		else:
			print('   [Wifi-GVA-Control]: Wifi connection already disabled. Nothing to do')
			return 0

	#def disableWifi

	def updateAlumnatPassword(self,password,confirmPassword):

		if self._checkPassword(password,confirmPassword):
			return 0
		else:
			if password!=self.currentAlumnatPassword:
				if not self.unattendedMode:
					response=input('   [Wifi-GVA-Control]: Do you want to update the password of the alumnat user? (yes/no)): ').lower()
				else:
					response='yes'
					
				if response.startswith('y'):
					try:
						self.writeLog("Changes in configuration of Wifi GVA:")
						self.writeLog('- Action: update alumnat password')
						self.createClient()
						ret=self.n4dClient.WifiEduGva.set_autologin(password)
						self.writeLog("- Result: changes apply successful")
						print('   [Wifi-GVA-Control]: Action completed successfull')
						return 0

					except n4d.client.CallFailedError as e:
						self.writeLog("- Error applying changes: %s"%e.code)
						print('   [Wifi-GVA-Control]: Error. Unable to update password of alumnat user')
						return 1
				else:
					print('   [Wifi-GVA-Control]: Action canceled')
					return 0
			else:
				print('   [Wifi-GVA-Control]: Password of alumnat user already exists. Nothing to do')
				return 0
	
	#def updateAlumnatPassword

	def removeAlumnatPassword(self):

		if self.isAlumnatPasswordConfigured:
			if self.currentWifiConnection!=3:
				if not self.unattendedMode:
					response=input('   [Wifi-GVA-Control]: Do you want to remove the password of alumnat user? (yes/no)): ').lower()
				else:
					response='yes'

				if response.startswith('y'):
					try:
						self.writeLog("Changes in configuration of Wifi GVA:")
						self.writeLog('- Action: remove alumnat password')
						self.createClient()
						ret=self.n4dClient.WifiEduGva.set_autologin("")
						self.writeLog("- Result: changes apply successful")
						print('   [Wifi-GVA-Control]: Action completed successfull')
						self._getInfo("End")
						return 0

					except n4d.client.CallFailedError as e:
						self.writeLog("- Error applying changes: %s"%e.code)
						print('   [Wifi-GVA-Control]: Error. Unable to remove password of alumnat user')
						return 1
			else:
				print('   [Wifi-GVA-Control]: Password for alumnat user cannot be deleted because the AUTOLOGIN option is activated')
				return 0
		else:
			print('   [Wifi-GVA-Control]: Password for alumnat user already removed. Nothing to do')
			return 0

	#de removeAlumnatPassword

	def n4dUpdatePassword(self,password):

		if self.currentUser!="":
			print('   [Wifi-GVA-Control]: Option valid only for schedled password changes')
			return 0
		else:
			if self.isAlumnatPasswordConfigured:
				try:
					self.writeLog("Changes in configuration of Wifi GVA:")
					self.writeLog('- Action: update alumnat password (with n4d one-shot)')
					self.createClient()
					tmpPassword=codecs.decode(password,'rot13')
					ret=self.n4dClient.WifiEduGva.set_autologin(tmpPassword)
					self.writeLog("- Result: changes apply successful")
					print('   [Wifi-GVA-Control]: Action completed successfull')
					self._getInfo("End")
					return 0

				except n4d.client.CallFailedError as e:
					self.writeLog("- Error applying changes: %s"%e.code)
					print('   [Wifi-GVA-Control]: Error. Unable to update password of alumnat user')
					return 1
			else:
				return 0

	#def n4dUpdatePassword

	def _getInfo(self,step="Initial"):

		'''
			Values:
				- 0: Disable
				- 1: WIFI_PROF
				- 2: WIFI_ALU
				- 3: AUTOLOGIN
		'''

		try:
			self.writeLog("Wifi Control. %s configuration"%step)
			wifiConfiguration=self.n4dClient.WifiEduGva.get_settings()
			wifiPassword=self.n4dClient.WifiEduGva.get_autologin()
			self.isAutologinConfigured=self._checkIfAutologinIsEnabled()

			if wifiConfiguration in [0,1,2,3]:
				if wifiConfiguration==0:
					self.isWifiConnectionEnabled=False
					self.currentWifiConnection=2
				else:
					self.isWifiConnectionEnabled=True
					self.currentWifiConnection=wifiConfiguration

			if wifiPassword==None:
				self.isAlumnatPasswordConfigured=False
			elif wifiPassword=="":
				self.isAlumnatPasswordConfigured=False
			else:
				self.isAlumnatPasswordConfigured=True
				self.currentAlumnatPassword=wifiPassword

			self.writeLog("- Current Wifi Option: %s"%(wifiConfiguration))
			self.writeLog("- Password for alumnat user configured: %s"%(str(self.isAlumnatPasswordConfigured)))
			
			return True

		except Exception as e:
			self.writeLog("- Error loading configuration: %s"%(str(e)))
			return False

	#def _getInfo

	def _mappingWifiOption(self,wifiOption,mappingType):

		if mappingType=="TextToInt":
			if wifiOption=="WIFI_PROF":
				return 1
			elif wifiOption=="WIFI_ALU":
				return 2
			elif wifiOption=="ALUMNAT":
				return 3
			else:
				return -1
		else:
			if wifiOption==1:
				return "WIFI_PROF"
			elif wifiOption==2:
				return "WIFI_ALU"
			elif wifiOption==3:
				return "ALUMNAT"

	#def _mappingWifiOption

	def _checkIfAutologinIsEnabled(self):

		try:
			ret=self.n4dclient.AlumnatAccountManager.get_alumnat_status()['status']
		except:
			ret=False

		return ret

	#def _checkIfAutologinIsEnabled

	def _checkPassword(self,password,confirmPassword):

		error=False

		if password=="" or password==None:
			print('   [Wifi-GVA-Control]: No password has been indicated for the alumnat user')
			error=True
		elif password!=confirmPassword:
			print('   [Wifi-GVA-Control]: The given passwords for the alumnat user do not match')
			error=True

		return error

	#def _checkPassword

	def _getCurrentUser(self):

		sudoUser=""
		loginUser=""
		pkexecUser=""

		try:
			sudoUser=(os.environ["SUDO_USER"])
		except:
			pass
		try:
			loginUser=os.getlogin()
		except:
			pass

		try:
			cmd="id -un $PKEXEC_UID"
			p=subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
			pkexecUser=p.communicate()[0].decode().strip()
		except Exception as e:
			pass

		if pkexecUser!="root" and pkexecUser!="":
			self.currentUser=pkexecUser

		elif sudoUser!="root" and sudoUser!="":
			self.currentUser=sudoUser
			
		else:
			self.currentUser=loginUser

		self.writeLog("Init session in lliurex-wifi-gva-control CLI")
		if loginUser!="":
			self.writeLog("User login in CLI: %s"%self.currentUser)
		else:
			self.writeLog("User login in CLI: No current user detected. A script may have been executed at login")

		self.writeLog("Unattended Mode:%s"%(str(self.unattendedMode)))

	#def _getCurrentUser

	def writeLog(self,msg):

		syslog.openlog("WIFI-GVA-CONTROL")
		syslog.syslog(msg)

	#def writeLog

#class WifiGvaControlCliManager	



