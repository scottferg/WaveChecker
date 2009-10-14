import pygtk
pygtk.require("2.0")
import gtk
import gtk.glade
import gobject

import threading
import time

import waveNotifier

gobject.threads_init()

class WaveCheckThread(threading.Thread):
    def __init__(self, username, password):
        self.username = username
        self.password = password

        threading.Thread.__init__(self)

    def run(self):
        # Check for updates every 10 minutes
        while True:
            self.check()
            time.sleep(30)

    def check(self):
        waveNotifier.login(self.username, self.password)

class WaveChecker:
    def makeToast(self, total, unread):
        '''
        Display a notification to the user with the number of unread blips
        '''
        pass

    def onLoginClicked(self, widget, data = None):
        self.username = self.txtUsername.get_text()
        self.password = self.txtPassword.get_text()

        self.thread = WaveCheckThread(self.username, self.password).start()
        self.window.hide()

    def onIconClick(self, widget, data = None):
        if self.window.get_property('visible'):
            self.window.hide()
        else:
            self.window.show()

    def onWindowClose(self, widget, data = None):
        self.window.hide()

    def showPopupMenu(self, widget, button, time, data = None): 
        if button == 3: 
            if data: 
                data.show_all() 
                data.popup(None, None, None, 3, time) 

    def __init__(self):
        self.username = None
        self.password = None

        glade = gtk.glade.XML('waveCheck.glade')

        self.txtUsername = glade.get_widget('txtUsername')
        self.txtPassword = glade.get_widget('txtPassword')
        self.btnLogin = glade.get_widget('btnLogin')
        self.window = glade.get_widget('mainWindow')

        menu = gtk.Menu() 
        menuItem = gtk.ImageMenuItem(gtk.STOCK_QUIT) 
        menuItem.connect('activate', lambda q: gtk.main_quit()) 
        menu.append(menuItem) 

        self.statusIcon = gtk.status_icon_new_from_file('wave.png')
        self.statusIcon.set_visible(True)

        self.statusIcon.connect('activate', self.onIconClick)
        self.statusIcon.connect('popup-menu', self.showPopupMenu, menu)
        self.window.connect('delete_event', lambda q: gtk.main_quit())

        glade.signal_autoconnect(self)

    def main(self):
        gtk.main()

if __name__ == '__main__':
    main = WaveChecker()
    main.main()
