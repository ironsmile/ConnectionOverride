#!/usr/bin/env python
# -*- coding: utf8 -*-
import _winreg as winreg
import wx
import conover


class MainWindow(wx.Frame):
    def __init__(self, parent, title):
        self.dirname = ''

        wx.Frame.__init__(self, parent, title=title)
        
        self.reg = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
        self.enabled = conover.check_enabled(self.reg)
        winreg.CloseKey(self.reg)
        
        self.sizer = None
        self.Center()
        self.draw()
    
    def draw(self):
        if self.enabled:
            button_text = "Disable"
            hint_label = "Connection override is on. Interface: %s" % self.enabled
        else:
            button_text = "Enable"
            hint_label = "Connection override is off."
        
        if self.sizer:
            self.sizer.Remove(self.button)
            self.button.Hide()
            self.sizer.Remove(self.hint)
            self.hint.Hide()
            self.sizer.Destroy()
        
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.hint = wx.StaticText(self, label=hint_label)
        self.sizer.Add(self.hint, 1, wx.CENTER, 5)
        
        self.button = wx.Button(self, -1, button_text)
        self.Bind(wx.EVT_BUTTON, self.change_state, self.button)
        self.sizer.Add(self.button, 1, wx.CENTER, 5)

        #Layout sizers
        self.SetSizer(self.sizer)
        self.sizer.Fit(self)
        self.Show()
    
    def change_state(self, event):
        self.reg = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
        if self.enabled:
            conover.disable(self.reg)
        else:
            conover.enable(self.reg)

        self.enabled = conover.check_enabled(self.reg)
        winreg.CloseKey(self.reg)
        self.draw()
        
    
if __name__ == "__main__":
    app = wx.App(redirect=1, filename='run.log')
    frame = MainWindow(None, "M$Live connection override")
    app.MainLoop()
