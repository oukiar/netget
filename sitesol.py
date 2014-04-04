from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.progressbar import ProgressBar

from network import Network

import json, socket, urllib, os

class Sitesol(GridLayout):
    def __init__(self, **kwargs):
        super(Sitesol, self).__init__(cols=2, **kwargs)
        
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
                
        #SERVER
        self.add_widget(Label(text='Server: ') )
        self.txt_serverip = TextInput(text=self.server_ip)
        self.add_widget(self.txt_serverip)
        
        #WAN IP
        self.lb_wan_ip = Label(text='Wan IP: ')
        self.add_widget(self.lb_wan_ip)
        self.txt_wan_ip = TextInput()
        self.add_widget(self.txt_wan_ip)
        
        #WAN PORT
        self.lb_wan_port= Label(text='Wan Port: ')
        self.add_widget(self.lb_wan_port)
        self.txt_wan_port = TextInput()
        self.add_widget(self.txt_wan_port)
        
        #separator
        self.add_widget(ProgressBar())
        self.add_widget(ProgressBar())
        
        
        #REMOTE IP
        self.lb_remote_ip = Label(text='Remote IP: ')
        self.add_widget(self.lb_remote_ip)
        self.txt_remote_ip = TextInput()
        self.add_widget(self.txt_remote_ip)
        
        #REMOTE PORT
        self.lb_remote_port= Label(text='Remote Port: ')
        self.add_widget(self.lb_remote_port)
        self.txt_remote_port = TextInput()
        self.add_widget(self.txt_remote_port)
        

        #separator
        self.add_widget(ProgressBar())
        self.add_widget(ProgressBar())
        
        
        #nickname
        self.add_widget(Label(text='Nick: ') )
        self.txt_nick = TextInput(text='your nickname')
        self.add_widget(self.txt_nick)
        
        #mensaje
        self.add_widget(Label(text='Mensaje: ') )
        self.txt_msg = TextInput()
        self.add_widget(self.txt_msg)
        
        
        
        #buttons
        self.btn_solveudp = Button(text='Resolver IP', 
                                    on_press=self.on_solveudp)
                                    
        self.add_widget(self.btn_solveudp)
        
        
        self.btn_sendmsg = Button(text='Enviar', 
                                    on_press=self.on_sendmsg)
                                    
        self.add_widget(self.btn_sendmsg)
        
        #history
        self.txt_messages = TextInput(text='Mensajes:')
        self.add_widget(self.txt_messages)
        
        
        #try to solve my udp info
        self.on_solveudp(None)
        
    def on_sendmsg(self, w):
        tosend = json.dumps({'msg':'message', 'data':self.txt_msg.text})
        self.net.send((self.txt_remote_ip.text, int(self.txt_remote_port.text)), tosend)
         
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
            
            ip, port = json.loads(data)
            
            self.txt_wan_ip.text = ip
            self.txt_wan_port.text = str(port)
            
        elif data_dict['msg'] == 'message':
            self.txt_messages.text += '\n' + data
            
            
               
if __name__ == '__main__':
    
    from kivy.base import runTouchApp
    
    client = Sitesol()
    runTouchApp(client)
    client.net.shutdown_network()
    
    
