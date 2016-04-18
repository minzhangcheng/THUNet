import sys
from PyQt4 import QtCore, QtGui, uic
import API.Login as AL

qtCreatorFile = "sim.ui"

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class MyApp(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.online = AL.online()
        self.state = dict()
        if self.online:
            self.state = AL.info()
        self.setupUi(self)
        self.setInfo()
        self.action.clicked.connect(self.change)

    def setInfo(self):
        if not AL.online():
            self.info.setText('You are currently offline.')
            self.action.setText('Connect')
            self.online = False
            self.state = dict()
        else:
            self.state = AL.info()
            infoText = 'You are currently online.\n'
            infoText += 'User: %s\n' % self.state['username']
            infoText += 'IP: %s\n' % self.state['ip']
            infoText += 'Usage: %f GB\n' \
                        % float(self.state['usage']/1024/1024/1024.0)
            infoText += 'Account Balance: %f' % self.state['money']
            self.info.setText(infoText)
            pro = int(self.state['usage']/1024/1024/1024.0)
            self.usage.setValue(int(self.state['usage']/1024/1024/1024.0))
            self.action.setText('Disconnect')
            self.online = True

    def change(self):
        if self.online:
            AL.logout()
            self.setInfo()
        else:
            AL.login(username=str(self.user.text()),
                     password=str(self.passwd.text()))
            self.setInfo()

    def __del__(self):
        AL.logout()


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())