#!/usr/bin/python
# -*- coding: latin-1 -*-

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

from network import Network
from database import Database

import json, socket, urllib, os

class SitesolServer(FloatLayout):
    def __init__(self, **kwargs):
        super(SitesolServer, self).__init__(**kwargs)

        #screen logger
        self.txt_log = TextInput(text='Netget server initiated')
        self.add_widget(self.txt_log)

        #actualizar en el servidor esta IP    
        r = urllib.urlopen('http://www.devsinc.com.mx/netget/server_ip.php?update_server_ip=foo')
         
