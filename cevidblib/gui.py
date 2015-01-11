# -*- coding: utf-8 -*-
""" cevidbtool - manage lists on CeviDB groups

Copyright 2014, Nicola Chiapolini v/o Carbon, carbon@cevi.ch

License: GNU General Public License version 3,
         or (at your option) any later version.

"""
from __future__ import division, print_function, unicode_literals

import wx
from wx.lib.rcsizer import RowColSizer
import os

class MainFrame(wx.Frame):

    def __init__(self, master, parent, title="mainframe"):
        """ main gui window """
        self._master = master

        wx.Frame.__init__(self, parent, title=title, size=(300,135))
        panel = wx.Panel(self)
        layout_table = RowColSizer()
        layout_table.AddGrowableCol(2)

        self.label_email = wx.StaticText(panel, -1, "Email:")
        layout_table.Add(self.label_email, row=1, col=1)
        self.email = wx.TextCtrl(panel, value=self._master.cfg.default_mail)
        layout_table.Add(self.email, row=1, col=2, flag=wx.EXPAND)

        self.label_pword = wx.StaticText(panel, -1, "Passwort:")
        layout_table.Add(self.label_pword, row=2, col=1)
        self.pword = wx.TextCtrl(panel, style=wx.TE_PASSWORD)
        layout_table.Add(self.pword, row=2, col=2, flag=wx.EXPAND)

        self.button_file = wx.Button(panel, label="Datei")
        self.Bind(wx.EVT_BUTTON, self.chooseFile, self.button_file)
        layout_table.Add(self.button_file, row=3, col=1)
        self.file = wx.TextCtrl(panel, style=wx.TE_READONLY)
        layout_table.Add(self.file, row=3, col=2, flag=wx.EXPAND)

        self.button_update = wx.Button(panel, label="aktualisieren")
        self.Bind(wx.EVT_BUTTON, self.runUpdate, self.button_update)
        layout_table.Add(self.button_update, row=4, col=2)

        layout_table.AddSpacer( 10, 1, row=1, col=3)
        panel.SetAutoLayout(True)
        panel.SetSizer(layout_table)
        panel.Layout()

        self.Show(True)

    def chooseFile(self, event):
        """ file dialog """
        dlg = wx.FileDialog(self, "Datei auswählen", os.path.expanduser("~"), "", "*.*", wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.file.WriteText(os.path.join(dlg.GetDirectory(),dlg.GetFilename()))
        dlg.Destroy()

    def runUpdate(self, event):
        """ main function and result message """
        message = ("Datei erfolgreich aktualisiert.", "OK.")
        try:
            self._master.run(self.email.GetValue(),
                             self.pword.GetValue(),
                             self.file.GetValue()
                            )
        except Exception as e:
            message = (e.message, "Error")
        dlg = wx.MessageDialog( self, message[0], message[1])
        dlg.ShowModal()
        dlg.Destroy()

