#!/usr/bin/python3

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QUrl
from PySide6.QtGui import QIcon
from PySide6.QtQml import QQmlApplicationEngine

import sys
import LliurexWifiControl

app = QApplication()
app.setDesktopFileName("lliurex-wifi-gva-control")
engine = QQmlApplicationEngine()
engine.clearComponentCache()
context=engine.rootContext()
wifiControlBridge=LliurexWifiControl.LliurexWifiControl(sys.argv[1])
context.setContextProperty("wifiControlBridge", wifiControlBridge)

url = QUrl("/usr/share/lliurex-wifi-gva-control/rsrc/lliurex-wifi-control.qml")

engine.load(url)
if not engine.rootObjects():
	sys.exit(-1)

engine.quit.connect(QApplication.quit)
ret=app.exec()
del engine
del app
sys.exit(ret)

