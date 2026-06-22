#!/usr/bin/python3

from PySide6.QtCore import QObject,Signal,Slot,QThread,Property,QTimer,Qt,QModelIndex,QUrl
from PySide6.QtGui import QDesktopServices
import os
import signal
import copy
import time
import N4dManager

signal.signal(signal.SIGINT, signal.SIG_DFL)

class GatherInfo(QThread):

	infoGathered=Signal(dict)

	def __init__(self,manager):

		super().__init__()
		self.manager=manager
	
	#def __init__
		
	def run(self,*args):
		
		time.sleep(0.2)
		ret=self.manager.loadConfig()
		self.infoGathered.emit(ret)

	#def run

#class GatherInfo

class UpdateInfo(QThread):

	infoUpdated=Signal(dict)

	def __init__(self,manager,info):

		super().__init__()
		self.manager=manager
		self.updateInfo=info

	#def __init__

	def run(self,*args):
		
		time.sleep(1)
		ret=self.manager.applyChanges(self.updateInfo)
		self.infoUpdated.emit(ret)
	
	#def run

#class UpdateInfo

class LliurexWifiControl(QObject):

	currentStackChanged=Signal()
	currentOptionsStackChanged=Signal()
	showSpinnerChanged=Signal()
	isWifiEnabledChanged=Signal()
	currentWifiOptionChanged=Signal()
	currentPasswordChanged=Signal()
	passwordEntryEnabledChanged=Signal()
	showEditPasswordBtnChanged=Signal()
	showConfirmPasswordChanged=Signal()
	errorInPasswordChanged=Signal()
	showClearPasswordBtnChanged=Signal()
	changesInWifiSettingsChanged=Signal()
	showSettingsMessageChanged=Signal()
	showChangesDialogChanged=Signal()
	showCDCWarningChanged=Signal()
	showPopUpChanged=Signal()
	closeGuiChanged=Signal()

	def __init__(self,ticket=None):

		super().__init__()
		self.initBridge(ticket)

	#def __init__

	@Property(int,notify=currentStackChanged)
	def currentStack(self):

		return self._currentStack

	#def currentStack

	@currentStack.setter
	def currentStack(self,currentStack):

		if self._currentStack!=currentStack:
			self._currentStack=currentStack
			self.currentStackChanged.emit()

	#def currentStack

	@Property(int, notify=currentOptionsStackChanged)
	def currentOptionsStack(self):

		return self._currentOptionsStack

	#def currentOptionsStack

	@currentOptionsStack.setter
	def currentOptionsStack(self,currentOptionsStack):

		if self._currentOptionsStack!=currentOptionsStack:
			self._currentOptionsStack=currentOptionsStack
			self.currentOptionsStackChanged.emit()

	#def currentOptionsStack

	@Property(bool,notify=showSpinnerChanged)
	def showSpinner(self):

		return self._showSpinner

	#def showSpinner

	@showSpinner.setter
	def showSpinner(self,showSpinner):

		if self._showSpinner!=showSpinner:
			self._showSpinner=showSpinner
			self.showSpinnerChanged.emit()

	#def showSpinner

	@Property(bool,notify=isWifiEnabledChanged)
	def isWifiEnabled(self):

		return self._isWifiEnabled

	#def isWifiEnabled

	@isWifiEnabled.setter
	def isWifiEnabled(self,isWifiEnabled):

		if self._isWifiEnabled!=isWifiEnabled:
			self._isWifiEnabled=isWifiEnabled
			self.isWifiEnabledChanged.emit()

	#def isWifiEnabled

	@Property(int,notify=currentWifiOptionChanged)
	def currentWifiOption(self):

		return self._currentWifiOption

	#def currentWifiOption

	@currentWifiOption.setter
	def currentWifiOption(self,currentWifiOption):

		if self._currentWifiOption!=currentWifiOption:
			self._currentWifiOption=currentWifiOption
			self.currentWifiOptionChanged.emit()

	#def currentWifiOption

	@Property(str,notify=currentPasswordChanged)
	def currentPassword(self):

		return self._currentPassword

	#def currentPassword

	@currentPassword.setter
	def currentPassword(self,currentPassword):

		if self._currentPassword!=currentPassword:
			self._currentPassword=currentPassword
			self.currentPasswordChanged.emit()

	#def currentPassword

	@Property(bool,notify=passwordEntryEnabledChanged)
	def passwordEntryEnabled(self):

		return self._passwordEntryEnabled

	#def passwordEntryEnabled

	@passwordEntryEnabled.setter
	def passwordEntryEnabled(self,passwordEntryEnabled):

		if self._passwordEntryEnabled!=passwordEntryEnabled:
			self._passwordEntryEnabled=passwordEntryEnabled
			self.passwordEntryEnabledChanged.emit()

	#def passwordEntryEnabled

	@Property(bool,notify=showEditPasswordBtnChanged)
	def showEditPasswordBtn(self):

		return self._showEditPasswordBtn

	#def showEditPasswordBtn

	@showEditPasswordBtn.setter
	def showEditPasswordBtn(self,showEditPasswordBtn):

		if self._showEditPasswordBtn!=showEditPasswordBtn:
			self._showEditPasswordBtn=showEditPasswordBtn
			self.showEditPasswordBtnChanged.emit()

	#def showEditPasswordBtn

	@Property(bool,notify=showConfirmPasswordChanged)
	def showConfirmPassword(self):

		return self._showConfirmPassword

	#def showConfirmPassword

	@showConfirmPassword.setter
	def showConfirmPassword(self,showConfirmPassword):

		if self._showConfirmPassword!=showConfirmPassword:
			self._showConfirmPassword=showConfirmPassword
			self.showConfirmPasswordChanged.emit()

	#def showConfirmPassword

	@Property(bool,notify=errorInPasswordChanged)
	def errorInPassword(self):

		return self._errorInPassword

	#def errorInPassword

	@errorInPassword.setter
	def errorInPassword(self,errorInPassword):

		if self._errorInPassword!=errorInPassword:
			self._errorInPassword=errorInPassword
			self.errorInPasswordChanged.emit()

	#def errorInPassword

	@Property(bool,notify=showClearPasswordBtnChanged)
	def showClearPasswordBtn(self):

		return self._showClearPasswordBtn

	#def showClearPasswordBtn

	@showClearPasswordBtn.setter
	def showClearPasswordBtn(self,showClearPasswordBtn):

		if self._showClearPasswordBtn!=showClearPasswordBtn:
			self._showClearPasswordBtn=showClearPasswordBtn
			self.showClearPasswordBtnChanged.emit()

	#def showClearPasswordBtn

	@Property(bool,notify=changesInWifiSettingsChanged)
	def changesInWifiSettings(self):

		return self._changesInWifiSettings

	#def changesInWifiSettings

	@changesInWifiSettings.setter
	def changesInWifiSettings(self,changesInWifiSettings):

		if self._changesInWifiSettings!=changesInWifiSettings:
			self._changesInWifiSettings=changesInWifiSettings
			self.changesInWifiSettingsChanged.emit()

	#def changesInWifiSettings

	@Property(dict,notify=showSettingsMessageChanged)
	def showSettingsMessage(self):

		return self._showSettingsMessage

	#def showSettingsMessage

	@showSettingsMessage.setter
	def showSettingsMessage(self,showSettingsMessage):

		if self._showSettingsMessage!=showSettingsMessage:
			self._showSettingsMessage=showSettingsMessage
			self.showSettingsMessageChanged.emit()

	#def showSettingsMessage

	@Property(bool,notify=showChangesDialogChanged)
	def showChangesDialog(self):

		return self._showChangesDialog

	#def showChangesDialog

	@showChangesDialog.setter
	def showChangesDialog(self,showChangesDialog):

		if self._showChangesDialog!=showChangesDialog:
			self._showChangesDialog=showChangesDialog
			self.showChangesDialogChanged.emit()

	#def showChangesDialog

	@Property(bool,notify=showCDCWarningChanged)
	def showCDCWarning(self):

		return self._showCDCWarning

	#def showCDCWarning

	@showCDCWarning.setter
	def showCDCWarning(self,showCDCWarning):

		if self._showCDCWarning!=showCDCWarning:
			self._showCDCWarning=showCDCWarning
			self.showCDCWarningChanged.emit()

	#def _showCDCWarning

	@Property(bool,notify=showPopUpChanged)
	def showPopUp(self):

		return self._showPopUp

	#def showPopUp	

	@showPopUp.setter
	def showPopUp(self,showPopUp):
		
		if self._showPopUp!=showPopUp:
			self._showPopUp=showPopUp		
			self.showPopUpChanged.emit()

	#def showPopUp

	@Property(bool, notify=closeGuiChanged)
	def closeGui(self):

		return self._closeGui

	#def closeGui	

	@closeGui.setter
	def closeGui(self,closeGui):
		
		if self._closeGui!=closeGui:
			self._closeGui=closeGui		
			self.closeGuiChanged.emit()

	#def _closeGui

	def initBridge(self,ticket):

		self.n4dMan=N4dManager.N4dManager()
		self._changesInWifiSettings=False
		self._showSettingsMessage={"show":False,"msgCode":"","type":""}
		self._showChangesDialog=False
		self._closeGui=False
		self._showPopUp=True
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
		self._showClearPasswordBtn=False
		self._showCDCWarning=False
		self.changeInActivation=False
		self.changeInOption=False
		self.changeInPassword=False
		self.initialPassword=True
		self.passwordCleared=False
		self.n4dMan.setServer(ticket)
		self.gatherInfoT=GatherInfo(self.n4dMan)
		self.gatherInfoT.start()
		self.gatherInfoT.infoGathered.connect(self._loadConfig)
		self.gatherInfoT.finished.connect(self.gatherInfoT.deleteLater)

	#def initBridge

	@Slot(dict)
	def _loadConfig(self,ret):		

		if not ret.get("status"):
			if self.currentStack==0:
				self.showSpinner=False
			else:
				self.showSettingsMessage={"show":True,"msgCode":ret.get("code"),"type":ret.get("type")}
		else:
			self._loadVars()
			self.currentStack=1

	#def _loadConfig

	def _loadVars(self):

		self.isWifiEnabled=self.n4dMan.isWifiEnabled
		self.currentWifiOption=self.n4dMan.currentWifiOption
		self.currentPassword=self.n4dMan.currentPassword
		self.initialPassword=True
		self.errorInPassword=False
		self.passwordEntryEnabled=False
		self.showSettingsMessage={"show":False,"msgCode":"","type":""}
		self.showClearPasswordBtn=False
		self.showEditPasswordBtn=False
		self.passwordCleared=False

		if self.isWifiEnabled and self.currentWifiOption==3:
			if not self.currentPassword:
				self.passwordEntryEnabled=True
				self.errorInPassword=True
				self.initialPassword=False
				self.showSettingsMessage={"show":True,"msgCode":self.n4dMan.ERROR_PASSWORD_EMPTY,"type":self.n4dMan.KIRIGAMI_MSG_ERROR}
			else:
				self.showEditPasswordBtn=True
		else:
			if self.isWifiEnabled and not self.n4dMan.getIntegrationCDCStatus():
				self.showSettingsMessage={"show":True,"msgCode":self.n4dMan.WARNING_CDC_ACTIVATION_REQUIRED,"type":self.n4dMan.KIRIGAMI_MSG_WARNING}
			
			self._manageClearPasswordBtn()

	#def _loadVars

	def _manageClearPasswordBtn(self):

		hasPassword=bool(self.currentPassword)
		notOption3OrDisabled=(self.currentWifiOption!=3 or not self.isWifiEnabled)
		
		self.showClearPasswordBtn=hasPassword and notOption3OrDisabled

	#def _manageClearPasswordBtn

	@Slot(bool)
	def manageWifiControl(self,value):

		self.showSettingsMessage={"show":False,"msgCode":"","type":""}
		if value!=self.isWifiEnabled:
			self.changeInActivation=(value!=self.n4dMan.isWifiEnabled)
			self.isWifiEnabled=value

		else:
			self.changeInActivation=False

		self._manageChanges()
		self._undoChangesInPassword()
		self._manageClearPasswordBtn()
		
	#def manageWifiControl

	@Slot(int)
	def manageWifiOptions(self,value):

		self.showSettingsMessage={"show":False,"msgCode":"","type":""}

		if value!=self.currentWifiOption:
			self.changeInOption=(value!=self.n4dMan.currentWifiOption)
			self.currentWifiOption=value
		else:
			self.changeInOption=False

		self._manageChanges()
		self._undoChangesInPassword()
		self._manageClearPasswordBtn()

	#def manageWifiOptions
	
	@Slot(dict)
	def changeInConfirmPasswordEntry(self,value):

		if not self.initialPassword and self.passwordEntryEnabled:
			self._managePassword(value)
	
	#def changeInConfirmPasswordEntry

	@Slot(dict)
	def changeInPasswordEntry(self,value):

		matchError=False

		if not self.initialPassword:
			self.showConfirmPassword=True
			if value.get("password"):
				self._managePassword(value)
			else:
				matchError=True
		else:
			if not value.get("password") and self.isWifiEnabled and self.currentWifiOption==3:
				matchError=True
			
		if matchError:
			self.errorInPassword=True
			self.showSettingsMessage={"show":False,"msgCode":"","type":""}

		self.initialPassword=False

	#def changeInPasswordEntry

	def _managePassword(self,value):

		passwordEntry=value.get("password")
		confirmPassword=value.get("confirmPassword")

		if passwordEntry!=confirmPassword:
			self.errorInPassword=True
			if passwordEntry and confirmPassword:
				self.showSettingsMessage={"show":True,"msgCode":self.n4dMan.ERROR_PASSWORDS_NOT_MATCH,"type":self.n4dMan.KIRIGAMI_MSG_ERROR}
			else:
				self.showSettingsMessage={"show":False,"msgCode":"","type":""}
			return

		if passwordEntry:
			
			self.showSettingsMessage={"show":False,"msgCode":"","type":""}
			self.errorInPassword=False
			
			if passwordEntry!=self.currentPassword:
				self.changeInPassword=(passwordEntry!=self.n4dMan.currentPassword)
				self.currentPassword=passwordEntry
				
			else:
				self.changeInPassword=False
					
			self._manageChanges()

	#def _managePassword

	@Slot()
	def editPasswordBtn(self):

		if self.currentWifiOption==3:
			self.passwordEntryEnabled=not self.passwordEntryEnabled
			self.initialPassword=False

	#def editPasswordBtn

	def _manageChanges(self):

		if self.changeInActivation:
			self.changesInWifiSettings=True
			return

		if self.isWifiEnabled:
			self.changesInWifiSettings=(self.changeInOption or self.changeInPassword)
			return
			
		self.changesInWifiSettings=(self.changeInPassword and self.passwordCleared)
	
	#def _manageChanges

	def _undoChangesInPassword(self):

		self.initialPassword=True

		if not self.passwordCleared or self.currentWifiOption==3:
			self.currentPassword=self.n4dMan.currentPassword
			if self.passwordCleared:
				self.passwordCleared=False

		self.showSettingsMessage={"show":False,"msgCode":"","type":""}
		self.initialPassword=False
		self.changeInPassword=False

		if not self.isWifiEnabled or self.currentWifiOption!=3:
			self.passwordEntryEnabled=False
			self.showConfirmPassword=False
			self.showEditPasswordBtn=False
			self.errorInPassword=False
			return

		if not self.currentPassword:
			self.passwordEntryEnabled=True
			if self.n4dMan.currentPassword:
				self.errorInPassword=True
				self.showSettingsMessage={"show":True,"msgCode":self.n4dMan.ERROR_PASSWORD_EMPTY,"type":self.n4dMan.KIRIGAMI_MSG_ERROR}
		else:
			self.showEditPasswordBtn=True

	#def _undoChangesInPassword

	@Slot()
	def applyChanges(self):

		nextStep=True

		if self.isWifiEnabled and self.changeInOption and self.currentWifiOption==3 and not self.currentPassword:
			self.showSettingsMessage={"show":True,"msgCode":self.n4dMan.ERROR_PASSWORD_EMPTY,"type":self.n4dMan.KIRIGAMI_MSG_ERROR}
			self.showChangesDialog=False
			return
					
		self.showSettingsMessage={"show":False,"msgCode":"","type":""}
		self.showPopUp=True
		self.showChangesDialog=False
		info={
			"isWifiEnabled":self.isWifiEnabled,
			"currentWifiOption":self.currentWifiOption,
			"currentPassword":self.currentPassword
		}
		self.updateInfoT=UpdateInfo(self.n4dMan,info)
		self.updateInfoT.start()
		self.updateInfoT.infoUpdated.connect(self._updateInfoRet)
		self.updateInfoT.finished.connect(self.updateInfoT.deleteLater)

	#def applyChanges	

	@Slot(dict)
	def _updateInfoRet(self,ret):

		if not ret.get("status"):
			self.closeGui=False
			self.showSettingsMessage={"show":True,"msgCode":ret.get("code"),"type":ret.get("type")}
			return

		self._initForm()
		self.showSettingsMessage={"show":True,"msgCode":ret.get("code"),"type":ret.get("type")}
		self.closeGui=True

		if self.isWifiEnabled and self.currentWifiOption!=3: 
			if not self.n4dMan.getIntegrationCDCStatus():
				self.showCDCWarning=True
				self.closeGui=False
	
	#def _updateInfoRet

	def _initForm(self):

		self._loadVars()
		self.changeInActivation=False
		self.changesInWifiSettings=False
		self.showConfirmPassword=False
		self.changeInPassword=False
		self.changeInOption=False
		self.showPopUp=False
		self.closeGui=not self.errorInPassword

	#def _initForm

	@Slot()
	def manageCDCWarning(self):

		self.showCDCWarning=False
		self.closeGui=True

	#def manageCDCWarning	

	@Slot()
	def cancelChanges(self):

		self.showChangesDialog=False
		self.showSettingsMessage={"show":False,"msgCode":"","type":""}
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

	@Slot()
	def clearPassword(self):

		self.showSettingsMessage={"show":False,"msgCode":"","type":""}
		self.initialPassword=True
		self.currentPassword=""
		self.changeInPassword=True
		self.passwordCleared=True
		self.showClearPasswordBtn=False
		self._manageChanges()

	#def clearPassword

	@Slot(int)
	def manageTransitions(self,stack):

		if self.currentOptionsStack!=stack:
			self.currentOptionsStack=stack

	#def manageTransitions
	
	@Slot()
	def openHelp(self):
		
		helpUrl='https://wiki.edu.gva.es/lliurex/tiki-index.php?page=Integración+con+las+WiFis+educativas+de+la+GVA'
		QDesktopServices.openUrl(QUrl(helpUrl))

	#def openHelp

	@Slot()
	def closeApplication(self):

		self.closeGui=False

		if self.errorInPassword:
			return

		if self.changesInWifiSettings:
			self.showChangesDialog=True
		else:
			self.closeGui=True
			self.n4dMan.writeLog("Close Session")

	#def closeApplication
	
#class LliurexWifiControl

