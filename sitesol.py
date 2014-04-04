from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label

from network import Network

import json, socket, urllib, os

class Sitesol(FloatLayout):
    def __init__(self, **kwargs):
        super(Sitesol, self).__init__(**kwargs)
        
        #get network instance from kwargs (arguments by keyword) or create a new network object
        self.net = kwargs.get('net', Network() )
        
        #exist connection?
        if not self.net.has_connection():
            #create a new connection
            self.net.create_connection(self.receiver)
        
        #obtener ip del servidor que resuelve tu ip:puerto UDP de internet
        response = urllib.urlopen('http://www.devsinc.com.mx/netget/solvers.php?get_server_ip=foo')
        self.server_ip = response.read()
        self.server_port = 31415
        
        #guardar nuestra informacion de conexion respecto a internet (WAN connection)
        self.inet_ip = None
        self.inet_port = None
        
        self.add_widget(Label(text='Server: '+self.server_ip) )
        
        self.btn_solveudp = Button(text='Get My IP', 
                                    on_press=self.on_solveudp, 
                                    size_hint=(None,None))
                                    
        self.add_widget(self.btn_solveudp)
        
    def on_solveudp(self, w):
        
        tosend = json.dumps({'msg':'get_inet_addr', 'data':None})
        self.net.send((self.server_ip, self.server_port), tosend)
         
    def receiver(self, data, addr):
        #unpack
        data_dict = json.loads(data)

        #extract data
        data = data_dict['data']
        
        #analize
        if data_dict['msg'] == 'ping':
            tosend = json.dumps({'msg':'ping_ack', 'data':socket.gethostname()})
            self.net.send(addr, tosend)
        elif data_dict['msg'] == 'addr_udp':
            print data
            
               
if __name__ == '__main__':
    
    from kivy.base import runTouchApp
    
    client = Sitesol()
    runTouchApp(client)
    client.net.shutdown_network()
    
    
