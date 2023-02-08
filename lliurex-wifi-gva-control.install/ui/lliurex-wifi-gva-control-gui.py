#!/usr/bin/python3

from PySide2.QtWidgets import QApplication
from PySide2.QtCore import QUrl
from PySide2.QtGui import QIcon
from PySide2.QtQml import QQmlApplicationEngine

import sys
import LliurexWifiControl

app = QApplication()
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
app.setWindowIcon(QIcon("/usr/share/icons/hicolor/scalable/apps/lliurex-wifi-gva-control.svg"));
ret=app.exec_()
del engine
del app
sys.exit(ret)

