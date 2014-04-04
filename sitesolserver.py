#!/usr/bin/python
# -*- coding: latin-1 -*-

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

from network import Network

import json, socket, urllib, os

class SitesolServer(FloatLayout):
    def __init__(self, **kwargs):
        super(SitesolServer, self).__init__(**kwargs)
        
        #get network instance from kwargs (arguments by keyword) or create a new network object
        self.net = kwargs.get('net', Network() )
        
        #exist connection?
        if not self.net.has_connection():
            #create a new connection
            self.net.create_connection(self.receiver)

        #screen logger
        self.txt_log = TextInput(text='Netget server initiated')
        self.add_widget(self.txt_log)

        #actualizar en el servidor esta IP    
        r = urllib.urlopen('http://www.devsinc.com.mx/netget/solvers.php?set_server_ip=foo')
         
    def receiver(self, data, addr):
        #unpack
        data_dict = json.loads(data)
        
        self.txt_log.text += '\nMessage: ' + data_dict['msg'] + ' from ' + addr[0] + ':' + str(addr[1])
        
        
        data = data_dict['data']
        
        #analize
        if data_dict['msg'] == 'ping':
            tosend = json.dumps({'msg':'ping_ack', 'data':socket.gethostname()})
            self.net.send(addr, tosend)
        elif data_dict['msg'] == 'get_inet_addr':            
            tosend = json.dumps({'msg':'addr_udp', 'data':json.dumps(addr)})
            self.net.send(addr, tosend)
            
if __name__ == '__main__':
    from kivy.base import runTouchApp
    
    
    server = SitesolServer()
    runTouchApp(server)
    server.net.shutdown_network()
            
