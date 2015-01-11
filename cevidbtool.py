#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" cevidbtool - manage lists on CeviDB groups

Copyright 2014, Nicola Chiapolini v/o Carbon, carbon@cevi.ch

License: GNU General Public License version 3,
         or (at your option) any later version.

"""
import sys
sys.path.append('./imports/')

import wx
from cevidblib.master import Master
from cevidblib.gui import MainFrame

app = wx.App(False)
master = Master()
gui    = MainFrame(master, None, 'CeviDB Tool')
app.MainLoop()
