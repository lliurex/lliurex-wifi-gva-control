#!/usr/bin/python3

from PySide2.QtCore import QObject,Signal,Slot,QThread,Property,QTimer,Qt,QModelIndex
import os
import threading
import signal
import copy
import time
import N4dManager

signal.signal(signal.SIGINT, signal.SIG_DFL)

class GatherInfo(QThread):

	def __init__(self,*args):

		QThread.__init__(self)
	
	#def __init__
		

	def run(self,*args):
		
		time.sleep(1)
		self.ret=LliurexWifiControl.n4dMan.loadConfig()

	#def run

#class GatherInfo

class UpdateInfo(QThread):

	def __init__(self,*args):

		QThread.__init__(self)

		self.updateInfo=args[0]
		self.ret=[]

	#def __init__

	def run(self,*args):
		
		time.sleep(1)
		self.ret=LliurexWifiControl.n4dMan.applyChanges(self.updateInfo)
	
	#def run

#class UpdateInfo

class LliurexWifiControl(QObject):

	n4dMan=N4dManager.N4dManager()

	def __init__(self,ticket=None):

		QObject.__init__(self)
		self.initBridge(ticket)

	#def __init__

	def initBridge(self,ticket):

		self._settingsWifiChanged=False
		self._showSettingsMessage=[False,"","Success"]
		self._showChangesDialog=False
		self._closeGui=False
		self._closePopUp=True
		self._currentStack=0
		self._currentOptionsStack=0
		self._isWifiEnabled=False
		self._currentWifiOption=0
		self._currentPassword=""
		self._passwordEntryEnabled=False
		self._showConfirmPassword=False
		self._showEditPasswordBtn=False
		self._errorInPassword=False
		self._showSpinner=True
		self.changeInActivation=False
		self.changeInOption=False
		self.changeInPassword=False
		self.initialPassword=True
		LliurexWifiControl.n4dMan.setServer(ticket)
		self.gatherInfo=GatherInfo()
		self.gatherInfo.start()
		self.gatherInfo.finished.connect(self._loadConfig)

	#def initBridge

	def _loadConfig(self):		

		if self.gatherInfo.ret:
			self.isWifiEnabled=copy.deepcopy(LliurexWifiControl.n4dMan.isWifiEnabled)
			self.currentWifiOption=copy.deepcopy(LliurexWifiControl.n4dMan.currentWifiOption)
			self.currentPassword=copy.deepcopy(LliurexWifiControl.n4dMan.currentPassword)
			self.initialPassword=True
			self.errorInPassword=False
			self.passwordEntryEnabled=False
			
			if self.isWifiEnabled and self.currentWifiOption==3:
				if self.currentPassword=="":
					self.passwordEntryEnabled=True
					self.errorInPassword=True
					self.initialPassword=False
					self.showSettingsMessage=[True,LliurexWifiControl.n4dMan.ERROR_PASSWORD_EMPTY,"Error"]
				else:
					self.showEditPasswordBtn=True
					self.showSettingsMessage=[False,"","Success"]
			else:
				self.showSettingsMessage=[False,"","Success"]

			self.currentStack=1
		else:
			if self.currentStack==0:
				self.showSpinner=False
			else:
				self.showSettingsMessage=[True,LliurexWifiControl.n4dMan.ERROR_LOADING_CONFIGURATION,"Error"]

	#def _loadConfig

	def _getCurrentStack(self):

		return self._currentStack

	#def _getCurrentStack

	def _setCurrentStack(self,currentStack):

		if self._currentStack!=currentStack:
			self._currentStack=currentStack
			self.on_currentStack.emit()

	#def _setCurrentStack

	def _getCurrentOptionsStack(self):

		return self._currentOptionsStack

	#def _getCurrentOptionsStack

	def _setCurrentOptionsStack(self,currentOptionsStack):

		if self._currentOptionsStack!=currentOptionsStack:
			self._currentOptionsStack=currentOptionsStack
			self.on_currentOptionsStack.emit()

	#def _setCurrentOptionsStack

	def _getShowSpinner(self):

		return self._showSpinner

	#def _getShowSpinner

	def _setShowSpinner(self,showSpinner):

		if self._showSpinner!=showSpinner:
			self._showSpinner=showSpinner
			self.on_showSpinner.emit()

	#def _setShowSpinner

	def _getIsWifiEnabled(self):

		return self._isWifiEnabled

	#def _getIsWifiEnabled

	def _setIsWifiEnabled(self,isWifiEnabled):

		if self._isWifiEnabled!=isWifiEnabled:
			self._isWifiEnabled=isWifiEnabled
			self.on_isWifiEnabled.emit()

	#def _setIsWifiEnabled

	def _getCurrentWifiOption(self):

		return self._currentWifiOption

	#def _getCurrentWifiOption

	def _setCurrentWifiOption(self,currentWifiOption):

		if self._currentWifiOption!=currentWifiOption:
			self._currentWifiOption=currentWifiOption
			self.on_currentWifiOption.emit()

	#def _setCurrentWifiOption

	def _getCurrentPassword(self):

		return self._currentPassword

	#def _getCurrentPassword

	def _setCurrentPassword(self,currentPassword):

		if self._setCurrentPassword!=currentPassword:
			self._currentPassword=currentPassword
			self.on_currentPassword.emit()

	#def _setCurrentPassword

	def _getPasswordEntryEnabled(self):

		return self._passwordEntryEnabled

	#def _getPasswordEntryEnabled

	def _setPasswordEntryEnabled(self,passwordEntryEnabled):

		if self._passwordEntryEnabled!=passwordEntryEnabled:
			self._passwordEntryEnabled=passwordEntryEnabled
			self.on_passwordEntryEnabled.emit()

	#def _setPasswordEntryEnabled

	def _getShowEditPasswordBtn(self):

		return self._showEditPasswordBtn

	#def _getShowEditPasswordBtn

	def _setShowEditPasswordBtn(self,showEditPasswordBtn):

		if self._showEditPasswordBtn!=showEditPasswordBtn:
			self._showEditPasswordBtn=showEditPasswordBtn
			self.on_showEditPasswordBtn.emit()

	#def _setShowEditPasswordBtn

	def _getShowConfirmPassword(self):

		return self._showConfirmPassword

	#def _getShowConfirmPassword

	def _setShowConfirmPassword(self,showConfirmPassword):

		if self._showConfirmPassword!=showConfirmPassword:
			self._showConfirmPassword=showConfirmPassword
			self.on_showConfirmPassword.emit()

	#def _setShowConfirmPassword

	def _getErrorInPassword(self):

		return self._errorInPassword

	#def _getErrorInPassword

	def _setErrorInPassword(self,errorInPassword):

		if self._errorInPassword!=errorInPassword:
			self._errorInPassword=errorInPassword
			self.on_errorInPassword.emit()

	#def _setErrorInPassword
	
	def _getShowSettingsMessage(self):

		return self._showSettingsMessage

	#def _getShowSettingsMessage

	def _setShowSettingsMessage(self,showSettingsMessage):

		if self._showSettingsMessage!=showSettingsMessage:
			self._showSettingsMessage=showSettingsMessage
			self.on_showSettingsMessage.emit()

	#def _setShowSettingsMessage

	def _getShowChangesDialog(self):

		return self._showChangesDialog

	#def _showChangesDialog

	def _setShowChangesDialog(self,showChangesDialog):

		if self._showChangesDialog!=showChangesDialog:
			self._showChangesDialog=showChangesDialog
			self.on_showChangesDialog.emit()

	#def _setShowChangesDialog

	def _getSettingsWifiChanged(self):

		return self._settingsWifiChanged

	#def _getSettingsWifiChanged

	def _setSettingsWifiChanged(self,settingsWifiChanged):

		if self._settingsWifiChanged!=settingsWifiChanged:
			self._settingsWifiChanged=settingsWifiChanged
			self.on_settingsWifiChanged.emit()

	#def _setSettingsWifiChanged

	def _getClosePopUp(self):

		return self._closePopUp

	#def _getClosePopUp	

	def _setClosePopUp(self,closePopUp):
		
		if self._closePopUp!=closePopUp:
			self._closePopUp=closePopUp		
			self.on_closePopUp.emit()

	#def _setClosePopUp	

	def _getCloseGui(self):

		return self._closeGui

	#def _getCloseGui	

	def _setCloseGui(self,closeGui):
		
		if self._closeGui!=closeGui:
			self._closeGui=closeGui		
			self.on_closeGui.emit()

	#def _setCloseGui

	@Slot(bool)
	def manageWifiControl(self,value):

		self.showSettingsMessage=[False,"","Success"]
		if value!=self.isWifiEnabled:
			self.isWifiEnabled=value
			if self.isWifiEnabled!=LliurexWifiControl.n4dMan.isWifiEnabled:
				self.changeInActivation=True
			else:
				self.changeInActivation=False
		else:
			self.changeInActivation=False

		self._manageChanges()
		self._undoChangesInPassword()
		
	#def manageWifiControl

	@Slot(int)
	def manageWifiOptions(self,value):

		self.showSettingsMessage=[False,"","Success"]

		if value!=self.currentWifiOption:
			self.currentWifiOption=value
			if self.currentWifiOption!=LliurexWifiControl.n4dMan.currentWifiOption:
				self.changeInOption=True
			else:
				self.changeInOption=False
		else:
			self.changeInOption=False

		self._manageChanges()
		self._undoChangesInPassword()

	#def manageWifiOptions
	
	@Slot('QVariantList')
	def managePassword(self,value):

		if not self.initialPassword and self.passwordEntryEnabled:
			if value[0]!=value[1]:
				self.showSettingsMessage=[True,LliurexWifiControl.n4dMan.ERROR_PASSWORDS_NOT_MATCH,"Error"]
				self.errorInPassword=True
			else:
				if value[0]!="":
					self.showSettingsMessage=[False,"","Success"]
					self.errorInPassword=False
					if value[0]!=self.currentPassword:
						self.currentPassword=value[0]
						if self.currentPassword!=LliurexWifiControl.n4dMan.currentPassword:
							self.changeInPassword=True
						else:
							self.changeInPassword=False
					else:
						self.changeInPassword=False
				
				self._manageChanges()
	
	#def managePassword

	@Slot('QVariantList')
	def changeInPasswordEntry(self,value):

		if not self.initialPassword:
			self.showConfirmPassword=True
			if value[0]!="":
				if value[0]!=value[1]:
					self.errorInPassword=True
					self.showSettingsMessage=[True,LliurexWifiControl.n4dMan.ERROR_PASSWORDS_NOT_MATCH,"Error"]
				else:
					self.showSettingsMessage=[False,"","Success"]
					self.errorInPassword=False
			else:
				self.errorInPassword=True
				self.showSettingsMessage=[True,LliurexWifiControl.n4dMan.ERROR_PASSWORD_EMPTY,"Error"]
		else:
			if value[0]=="":
				if self.isWifiEnabled and self.currentWifiOption==3:
					self.errorInPassword=True
					self.showSettingsMessage=[True,LliurexWifiControl.n4dMan.ERROR_PASSWORD_EMPTY,"Error"]
			
		self.initialPassword=False

	#def changeInPasswordEntry

	@Slot()
	def editPasswordBtn(self):

		if self.currentWifiOption==3:
			self.passwordEntryEnabled=True
			self.initialPassword=False

	#def editPasswordBtn

	def _manageChanges(self):

		if self.changeInActivation:
			self.settingsWifiChanged=True
		else:
			if self.isWifiEnabled:
				if self.changeInOption or self.changeInPassword:
					self.settingsWifiChanged=True
				else:
					self.settingsWifiChanged=False
			else:
				self.settingsWifiChanged=False

	#def _manageChanges

	def _undoChangesInPassword(self):

		self.initialPassword=True
		self.currentPassword=LliurexWifiControl.n4dMan.currentPassword
		self.showSettingsMessage=[False,"","Success"]
		self.initialPassword=False
		self.changeInPassword=False

		if not self.isWifiEnabled:
			self.passwordEntryEnabled=False
			self.showConfirmPassword=False
			self.showEditPasswordBtn=False
			self.errorInPassword=False
		else:
			if self.currentWifiOption!=3:
				self.passwordEntryEnabled=False
				self.showConfirmPassword=False
				self.showEditPasswordBtn=False
				self.errorInPassword=False
			else:
				if self.currentPassword=="":
					self.passwordEntryEnabled=True
					self.errorInPassword=True
					self.showSettingsMessage=[True,LliurexWifiControl.n4dMan.ERROR_PASSWORD_EMPTY,"Error"]
				else:
					self.showEditPasswordBtn=True

	#def _undoChangesInPassword

	@Slot()
	def applyChanges(self):

		nextStep=True

		if self.changeInOption and self.currentWifiOption==3:
			if self.currentPassword=="":
				self.showSettingsMessage=[True,LliurexWifiControl.n4dMan.ERROR_PASSWORD_EMPTY,"Error"]
				if self.showChangesDialog:
					self.showChangesDialog=False
				nextStep=False
		if nextStep:
			self.showSettingsMessage=[False,"","Success"]
			self.closePopUp=False
			self.showChangesDialog=False
			infoToUpdate=[self.isWifiEnabled,self.currentWifiOption,self.currentPassword]
			self.updateInfoT=UpdateInfo(infoToUpdate)
			self.updateInfoT.start()
			self.updateInfoT.finished.connect(self._updateInfoRet)

	#def applyChanges	

	def _updateInfoRet(self):

		if self.updateInfoT.ret[0]:
			self._initForm()
			self.showSettingsMessage=[True,self.updateInfoT.ret[1],"Success"]
			self.closeGui=True
		else:
			self.showSettingsMessage=[True,self.updateInfoT.ret[1],"Error"]
			self.closeGui=False


	#def _updateInfoRet

	def _initForm(self):

		self._loadConfig()
		self.settingsWifiChanged=False
		#self.initialPassword=True
		self.showConfirmPassword=False
		#self.passwordEntryEnabled=False
		self.changeInPassword=False
		#self.errorInPassword=False
		self.closePopUp=True
		if self.errorInPassword:
			self.closeGui=False
		else:
			self.closeGui=True

	#def _initForm	

	@Slot()
	def cancelChanges(self):

		self.closePopUp=False
		self.showChangesDialog=False
		self.showSettingsMessage=[False,"","Success"]
		self._initForm()

	#def cancelChanges

	@Slot(str)
	def manageChangesDialog(self,action):
		
		if action=="Accept":
			self.applyChanges()
		elif action=="Discard":
			self.cancelChanges()
		elif action=="Cancel":
			self.closeGui=False
			self.showChangesDialog=False

	#def manageChangesDialog

	@Slot(int)
	def manageTransitions(self,stack):

		if self.currentOptionsStack!=stack:
			self.currentOptionsStack=stack

	#def manageTransitions
	
	@Slot()
	def openHelp(self):
		
		self.help_cmd='xdg-open https://wiki.edu.gva.es/lliurex/tiki-index.php?page=Lliurex-WIFI-GVA-Control'
		
		self.open_help_t=threading.Thread(target=self._openHelp)
		self.open_help_t.daemon=True
		self.open_help_t.start()

	#def openHelp

	def _openHelp(self):

		os.system(self.help_cmd)

	#def _openHelp

	@Slot()
	def closeApplication(self):

		self.closeGui=False
		if not self.errorInPassword:
			if self.settingsWifiChanged:
				self.showChangesDialog=True
			else:
				self.closeGui=True
				LliurexWifiControl.n4dMan.writeLog("Close Session")
		else:
			self.closeGui=False

	#def closeApplication
	
	on_currentStack=Signal()
	currentStack=Property(int,_getCurrentStack,_setCurrentStack, notify=on_currentStack)
	
	on_currentOptionsStack=Signal()
	currentOptionsStack=Property(int,_getCurrentOptionsStack,_setCurrentOptionsStack, notify=on_currentOptionsStack)

	on_showSpinner=Signal()
	showSpinner=Property(bool,_getShowSpinner,_setShowSpinner,notify=on_showSpinner)
	
	on_isWifiEnabled=Signal()
	isWifiEnabled=Property(bool,_getIsWifiEnabled,_setIsWifiEnabled,notify=on_isWifiEnabled)
	
	on_currentWifiOption=Signal()
	currentWifiOption=Property(int,_getCurrentWifiOption,_setCurrentWifiOption, notify=on_currentWifiOption)

	on_currentPassword=Signal()
	currentPassword=Property(str,_getCurrentPassword,_setCurrentPassword,notify=on_currentPassword)

	on_passwordEntryEnabled=Signal()
	passwordEntryEnabled=Property(bool,_getPasswordEntryEnabled,_setPasswordEntryEnabled,notify=on_passwordEntryEnabled)

	on_showEditPasswordBtn=Signal()
	showEditPasswordBtn=Property(bool,_getShowEditPasswordBtn,_setShowEditPasswordBtn,notify=on_showEditPasswordBtn)
	
	on_showConfirmPassword=Signal()
	showConfirmPassword=Property(bool,_getShowConfirmPassword,_setShowConfirmPassword,notify=on_showConfirmPassword)
	
	on_errorInPassword=Signal()
	errorInPassword=Property(bool,_getErrorInPassword,_setErrorInPassword,notify=on_errorInPassword)

	on_settingsWifiChanged=Signal()
	settingsWifiChanged=Property(bool,_getSettingsWifiChanged,_setSettingsWifiChanged, notify=on_settingsWifiChanged)

	on_showSettingsMessage=Signal()
	showSettingsMessage=Property('QVariantList',_getShowSettingsMessage,_setShowSettingsMessage,notify=on_showSettingsMessage)

	on_showChangesDialog=Signal()
	showChangesDialog=Property(bool,_getShowChangesDialog,_setShowChangesDialog,notify=on_showChangesDialog)

	on_closePopUp=Signal()
	closePopUp=Property(bool,_getClosePopUp,_setClosePopUp, notify=on_closePopUp)

	on_closeGui=Signal()
	closeGui=Property(bool,_getCloseGui,_setCloseGui, notify=on_closeGui)


#class LliurexWifiControl

