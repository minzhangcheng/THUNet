import sys
from PyQt5 import QtCore, QtWidgets, uic
import API.Login as AL

qtCreatorFile = "sim.ui"

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
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
            self.info.setText('您未登陆在线.')
            self.action.setText('连接')
            self.online = False
            self.state = dict()
        else:
            self.state = AL.info()
            infoText = '您已经登陆在线了.\n'
            infoText += '用户名: %s\n' % self.state['username']
            infoText += 'IP地址: %s\n' % self.state['ip']
            infoText += '已用流量: %f GB\n' \
                        % float(self.state['usage']/1024/1024/1024.0)
            infoText += '帐号余额: %f元' % self.state['money']
            self.info.setText(infoText)
            pro = int(self.state['usage']/1024/1024/1024.0)
            self.usage.setValue(int(self.state['usage']/1024/1024/1024.0))
            self.action.setText('断开连接')
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
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())