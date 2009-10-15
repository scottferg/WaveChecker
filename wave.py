import wx

try:
    import pynotify

    pynotify.init('Wave checker')
except ImportError:
    pass

try:
    import PySnarl
except ImportError:
    pass

import threading
import time
import os

import waveNotifier

class WaveCheckThread(threading.Thread):
    def __init__(self, username, password):
        self.username = username
        self.password = password

        threading.Thread.__init__(self)

    def run(self):
        # Check for updates every 30 minutes
        while True:
            self.check()
            time.sleep(1800)

    def check(self):
        if waveNotifier.login(self.username, self.password):
            result = waveNotifier.readInbox()

            try:
                uri = 'file://' + os.path.abspath(os.path.curdir) + '/wave_logo.png'
                pynotify.Notification('Google Wave', 'You have %s unread blips' % (result[1]), uri).show()
            except NameError:
                pass
            
            try:
                PySnarl.snShowMessage('Google Wave', 'You have %s unread blips' % (result[1]), 5, iconPath = os.getcwd() + '\wave_logo.png')
            except NameError:
                print 'Unread blips: %s' % result[1]

class WaveChecker:
    def onLoginClick(self, event):
        self.username = self.txtUsername.GetValue()
        self.password = self.txtPassword.GetValue()

        self.thread = WaveCheckThread(self.username, self.password).start()
        self.frame.Show(False)

    def onQuitClicked(self, event):
        if event.GetId() == wx.ID_EXIT:
            self.app.ExitMainLoop()

    def onIconClick(self, event):
        if self.frame.IsShown():
            self.frame.Show(False)
        else:
            self.frame.Show(True)

    def showPopupMenu(self, event):
        menu = wx.Menu()

        if (wx.Platform == '__WXMAC__'):
            wx.App.SetMacExitMenuItemId(wx.ID_EXIT)
        else:
            exitMenuItem = menu.Append(wx.ID_EXIT, 'Quit')

        wx.EVT_MENU(menu, wx.ID_EXIT, self.onQuitClicked)

        self.statusIcon.PopupMenu(menu)

    def __init__(self):
        self.username = None
        self.password = None

        self.app = wx.PySimpleApp()

        # Build the login window
        self.frame = wx.Frame(None, wx.ID_ANY, 'Google Wave Checker')

        vertical = wx.BoxSizer(wx.VERTICAL)
        horizontal = wx.BoxSizer(wx.HORIZONTAL)

        userLabel = wx.StaticText(self.frame, 1, 'Username:')
        self.txtUsername = wx.TextCtrl(self.frame, 3)
        horizontal.Add(userLabel, 0, wx.EXPAND)
        horizontal.Add(self.txtUsername, 1, wx.EXPAND)
        vertical.Add(horizontal, 0, wx.EXPAND)
        
        passwordLabel = wx.StaticText(self.frame, 2, 'Password:')
        self.txtPassword = wx.TextCtrl(self.frame, 4, style = wx.TE_PASSWORD)
        horizontal.Add(passwordLabel, 0, wx.EXPAND)
        horizontal.Add(self.txtPassword, 1, wx.EXPAND)
        vertical.Add(horizontal, 1, wx.EXPAND)

        self.btnLogin = wx.Button(self.frame, 5, 'Login')
        vertical.Add(self.btnLogin, 2, wx.EXPAND)

        self.frame.SetSizer(vertical)
        self.frame.SetAutoLayout(1)
        vertical.Fit(self.frame)

        # Create the taskbar icon
        icon = wx.Icon('wave.png', wx.BITMAP_TYPE_PNG)
        self.statusIcon = wx.TaskBarIcon()
        self.statusIcon.SetIcon(icon, 'Wave Checker')

        # Bind events
        wx.EVT_TASKBAR_RIGHT_UP(self.statusIcon, self.showPopupMenu)
        wx.EVT_TASKBAR_LEFT_UP(self.statusIcon, self.onIconClick)
        wx.EVT_BUTTON(self.btnLogin, 5, self.onLoginClick)

        self.app.MainLoop()

if __name__ == '__main__':
    main = WaveChecker()
