from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label


class Sitesol(FloatLAyout):
    def __init__(self, **kwargs):
        super(Sitesol, self).__init__(**kwargs)
        
        #get network instance from kwargs (arguments by keyword) or create a new network object
        self.net = kwargs.get('net', Network() )
        
        #exist connection?
        if not self.net.has_connection():
            #create a new connection
            self.net.create_connection(self.receiver)
        
        #obtener ip del servidor que resuelve tu ip:puerto de internet
        r = urllib.urlopen('http://www.devsinc.com.mx/netget/solvers.php?solveip=foo')
        
        self.server = 
        
        #guardar nuestra informacion de conexion respecto a internet
        self.inet_ip = 
        self.inet_port = 
        
        self.add_widget
    
    
if __name__ == '__main__':
    
    
    
