#!/usr/bin/python
# -*- coding: utf-8 -*-



from subprocess import check_output

import socket, sys, hashlib
from threading import Timer
from time import sleep



from kivy.clock import Clock

'''
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.accordion import Accordion, AccordionItem
from kivy.properties import StringProperty

from kivy.network.urlrequest import UrlRequest
'''

#from listbox import ListBox
#from database import Database

import os
import json
import threading

from math import ceil

#encryption ... disabled ... instead use ed25519
#from M2Crypto import RSA, Rand, EVP
import base64

#dont need more the www.devsinc.com.mx server
try:
    import netifaces
except:
    netifaces = None


from functools import partial

#http://www.effbot.org/librarybook/datetime.htm
import datetime
import time


#from utils import find_get_attr, get_hash, MessageBoxTime, ngDialog

'''
BETA 0.1
ALPHA 0.5
'''



'''
kivy on raspberry
http://wonderfulcode.tumblr.com/post/54102854344/kivy-on-raspberry-pi
'''


'''
Inicialmente netget intenta comunicar localmente
Despues internet
Finalmente se queda en modo RAW en todas las interfaces
'''

'''
Pendientes:
- Checar que los mensajes enviados, lleguen (checar en la recepcion o en el envio?, personalmente creo que quien envia, debe verificar que todos los paquetes de su envio hayan llegado (lo comprueba cuando recibe el ACK de su mensaje)
- Crear y manejar sesiones encriptadas una vez que el login ha sido correcto (handshake)
- Simple chat
- Interconnections between users (pending).
'''

'''
Netget networking stuff
     the netget soul is based on UDP
     we can talk all day about netget, and nobody can Imagine it
'''

'''
The netget phylosophy is: 'Securing people's communications'
and ... with the batteries included
'''

'''
Netget transmission packets
    Los paquetes son segmentados durante la transmision y reensamblados en la recepcion 
'''

'''
Netget data packets

    For incomming packets:
        - Can be encrypted with RSA2048 self public key
        - Encripted with AES256 session key (with respective client or user)
        
    For outgoing packets:
        - Can be encrypted with RSA2048 self private key
        - Encripted with AES256 session key (with respective client or user)

 - Packets can be:
    - Encripted with RSA 2048 public key (self), normally during login or new account process.
    - Encripted with RSA 4096 public key (self), normally when you use NETGET_SECURE_MODE.
    - Encripted with AES256 session key (related to a communication with specific user-client, not machines)
    - Additional if you are the server, packages can be encrypted using the Netget server public key (the base of our security) used during login and new account
    - And if youre the server, you must send encripted with server private key 

 - Packets json data format:
    msg:
        login
        data:
            user
            passhash
            
    msg:
        new_account
        data:
            user
            passhash
            privkey            Clave privada generada en el cliente y encriptada con AES256 con passphrase usando el password en texto plano
            
    msg:
        ping
        
    msg:
        ping_ack
        
    msg:
        solve_udp_info  
        
    msg:
        get_my_computers
        
    msg:
        get_my_friends
        
    msg:
        get_my_repositories
'''

'''
Netget presentation format
    - Widget in json format with information for create the widget
        that represent the presentation. (is the base of runtime netget
        interface serialization)
'''


import urllib


#fix it ... the udp packet overflow 512 bytes, check if this is a problem
udp_max_size=512    #with this value we think that the netget_packet never reach 512 bytes (UDP best minimal size) ... FIXME?


#research if is possible determinate the max udp size with a trick

netget_port = 31415

'''
RETRANSMISSION MODES

- Sin retransmission (elimina transmisiones pasadas completas e incompletas)
- Con retransmision rapida (Si inicia una transmission futura y existe alguna transmision incompleta, reenvia los paquetes que no hayan llegado, a menos que
            ya haya transcurrido el timeout)
- Con retransmission completa e integra (equiparable a TCP), se encarga de que todas las transmisiones sean completas

'''

def get_hash(text):
    cryptor = hashlib.sha512()
    if cryptor != None:
        cryptor.update(text)
        return cryptor.hexdigest()
        
class Transmission:
    def __init__(self, **kwargs):
        self.trans_id = kwargs.get('trans_id')
        self.packets = {}
        
    def send(self, data, bcrypt=False):
       
        #send the packet in parts of udp_max_size
        total_packets = ceil(len(data)/float(udp_max_size))
        
        packet_counter = 0

        #divide data in small packets
        for i in range(0, len(data), udp_max_size):
            #assemble the packet ... transmission_id is a 32 bits number that is unique by peer and is deleted 
            #once that transmission is complete
            '''
            data_dict = {'transmission_id':self.trans_id,
                        'data':data[i:i+udp_max_size],
                        'total_packets':total_packets,
                        'packet_number':packet_counter,
                        'encrypted':bcrypt,
                        'timeout':str(datetime.datetime.now()),
                        'attemps':1}
            '''
            
            data_dict = {'tr':self.trans_id,
                        'd':base64.b64encode(data[i:i+udp_max_size]),   #encoded because can broke the json packet conversion
                        'tp':total_packets,
                        'pn':packet_counter,
                        'e':bcrypt,
                        #'tm':str(datetime.datetime.now()),
                        'a':1}
                        
            self.packets[packet_counter] = data_dict
            
            packet_counter += 1
            
        #print 'Enviados ' + str(len(self.packets) ) + ' paquetes'
        
class Peer:
    def __init__(self, **kwargs):
        #super(Peer, self).__init__(**kwargs)
        
        self.ip =       kwargs.get('ip')
        self.port =     kwargs.get('port')
        self.addr =     (self.ip, self.port)
        
        
        #self.transmissions = BoxLayout()
        #self.content = self.transmissions
        
        self.transmissions = {}
        
        self.transmissions_counter = 0
        
        self.pubkey = None  #this key is valid when the peer respond the handshake
        
        #self.title = self.ip + ':' + str(self.port)
        
    def send(self, data):
                
        #el id de transmission es unico por peer y va incrementandose
        trans_id = str(self.transmissions_counter)
        
        #increment the counter of transmissions
        self.transmissions_counter = self.transmissions_counter + 1
        
        #crear transmission
        trans = Transmission(trans_id=trans_id)
        self.transmissions[trans_id] = trans
        
        
        #enviar datos usando el objeto transmission (divide la informacion en paquetes)
        trans.send(data)
        
        return trans
        
    def recv(self, data_dict):

        trans_id = data_dict['tr']
        
        #obtener la transmision correspondiente a este paquete
        if trans_id in self.transmissions:
            trans = self.transmissions[trans_id]
        else:
            trans = Transmission(trans_id=trans_id)
            self.transmissions[trans_id] = trans
                
        trans.packets[data_dict['pn']] = data_dict['d']    #append only the data of this packet
        
        return trans

class SendThread(threading.Thread):
    '''
    Send a packet using a shared queue with the main app (thread)
    '''
    def __init__(self, **kwargs):
        self.sock = kwargs.pop('sock')
        self.safe_pop_packet = kwargs.pop('safe_pop_packet')
        super(SendThread, self).__init__(**kwargs)
        
        self.shutlock = threading.Lock()
        
        self.finish_thread = False
        self.shuted_down = False

    def run(self):
        print 'Running sender thread'
        while True:
            try:
                packet_data = self.safe_pop_packet()
                
                #si no hubo paquetes
                if packet_data == None:
                    sleep(.01)
                    continue
                                        
                self.sock.sendto(packet_data[0], packet_data[1])   #packet_data holds (data, addr)

                #finalize this thread?
                self.shutlock.acquire()
                finish_thread = self.finish_thread
                self.shutlock.release()
                
                if finish_thread:
                    print 'Finishing SendThread'
                    break
                
            except socket.error as e:
                print 'Error en el thread send: ', e

        self.shuted_down = True
        
    def shutdown(self):
        self.shutlock.acquire()
        self.finish_thread = True
        self.shutlock.release()
        
    def is_shuted_down(self):
        self.shutlock.acquire()
        shuted_down = self.shuted_down 
        self.shutlock.release()
        
        return shuted_down

class NetworkOut:
    def __init__(self, **kwargs):
        
        self.peers = {}
        
        self.sock = kwargs.get('sock')
        
        #lock object for sinchronization
        self.lock = threading.Lock()
        
        #cola donde se almacenan los paquetes a enviar y que el hilo de envio estará extrayendo
        self.queue = []
        
        
        #hilo encargado de paquetes salientes (enviados)
        self.send_thread = SendThread(sock=self.sock, safe_pop_packet=self.safe_pop_packet)
        self.send_thread.start()
        
        
    def safe_pop_packet(self):
        '''
        Extrae un paquete desde la cola de paquetes a enviar de manera segura
        Warning: Esta funcion es solo usada por el hilo SendThread
        '''
        self.lock.acquire()
        if len(self.queue) > 0:
            packet = self.queue.pop(0)
        else:
            packet = None
        self.lock.release()
        
        return packet
        
    def safe_push_packet(self, packet_bin, addr):
        '''
        Agrega un paquete de manera segura a la cola de paquetes a enviar (que revisa asincronamente el hilo SendThread)
        '''
        self.lock.acquire()
        self.queue.append( (packet_bin, addr) )
        self.lock.release()
        
    def netget_friend_send(self, friend, msg, data):
        '''
        Send information to a friend (with previous handshake successfull)
        '''
        pass
        
    def netget_send(self, addr, msg, data=None):
        '''
        The best easy way to send information over netget (if you know the destination ip)
        '''
        #verificar que este corriendo aun el hilo de envio de mensajes
        if self.send_thread.is_shuted_down():
            return
                
        msg_dict = {'msg':msg, 'data':data}
        msg_json = json.dumps(msg_dict)
        self.send(addr, msg_json)
        
    def send(self, addr, data, bcrypt=False):
        '''
        Send data over UDP and store in the correct peer
        '''
        addrkey = (addr[0] + ':' + str(addr[1]) )
        
        if addrkey in self.peers:
            #obtener el objeto de este peer
            peer = self.peers[addrkey]
        else:
            #crear nuevo objeto que representa este peer
            peer = Peer( ip=addr[0], port=addr[1] ) 
            self.peers[addrkey] = peer
            
        #visualize
        transmission = peer.send(data)
        
        #enqueue all packets to queue (safe-thread)
        for packet in transmission.packets:
            packet_json = json.dumps(transmission.packets[packet])
            
            self.safe_push_packet(packet_json, addr)
            
class RecvThread(threading.Thread):
    '''
    Inform about new packets using a safe-thread callback function 
    '''
    def __init__(self, **kwargs):
        self.sock = kwargs.pop('sock')
        self.callback = kwargs.pop('callback')
        
        super(RecvThread, self).__init__(**kwargs)
        
        self.shutlock = threading.Lock()
        
        self.finish_thread = False
        self.shuted_down = False

    def run(self):
        print 'Running receiver thread ...'
        while True:
            try:
                #data, addr = self.sock.recvfrom(udp_max_size)
                data, addr = self.sock.recvfrom(1024)
                                
                self.callback(data, addr)
                

                #finalize this thread?
                self.shutlock.acquire()
                finish_thread = self.finish_thread
                self.shutlock.release()
                
                if finish_thread:
                    print 'Finishing RecvThread'
                    break
                
            except socket.error as e:
                print 'Error en el thread recv: ', e
                
        self.shuted_down = True
        self.sock.close()
                
    def shutdown(self):
        self.shutlock.acquire()
        self.finish_thread = True
        self.shutlock.release()
        
    def is_shuted_down(self):
        self.shutlock.acquire()
        shuted_down = self.shuted_down 
        self.shutlock.release()
        
        return shuted_down

class NetworkIn:
    def __init__(self, **kwargs):
        
        self.sock = kwargs.get('sock')

        self.dispatch_message = kwargs.get('dispatch_message')
        
        #self.peers = BoxLayout(orientation='vertical')
        #self.content = self.peers

        self.peers = {}

        #lock object for sinchronization
        self.lock = threading.Lock()
        
        #cola donde se almacena todo lo que proviene de la red
        self.queue = []
        
        #hilo encargado de paquetes entrantes
        self.recv_thread = RecvThread(sock=self.sock, callback=self.safe_recv)
        self.recv_thread.start()
    
        #check each interval of time if are new incoming packets
        Clock.schedule_interval(self.packet_assembler, .01)
        
        #super(NetworkIn, self).__init__(title='NetworkIn', **kwargs)
        
    def packet_assembler(self, dt):
        '''
        Funcion encargada de extraer paquetes recibidos de manera asincrona ...
        Nota: Verificar si el tiempo de intervalo nos da una velocidad de recepcion
            adecuada, de no ser asi, usar un while hasta extraer todos los paquetes 
            de la cola en cada intervalo
        '''
        packet, addr = self.pop_received_packet()
        
        #hasta que no haya paquetes
        while packet != None:
            #procesar paquete
            self.recv(packet, addr)
            
            #intentar obtener otro paquete
            packet, addr = self.pop_received_packet()
            
    def safe_recv(self, packet, addr):
        '''
        Recv packets queue (to process)
        
        Warning: This function is used only by the recv_thread for enqueue received packets (safe thread)
        '''
        self.lock.acquire()
        self.queue.append( (packet, addr) )
        self.lock.release()
        
    def pop_received_packet(self):
        '''
        Funcion usada por el hilo principal para extraer paquetes entrantes de manera segura (safe thread)
        '''
        self.lock.acquire()
        try:
            packet, addr = self.queue.pop(0)
        except:
            packet = None
            addr = None
        self.lock.release()
        
        return (packet, addr)
        
    def recv(self, data, addr):
        '''
        Recibe un paquete de datos en json listo para ser filtrado y agrupado adecuadamente (peer, transmission, packet)
        '''
                
        data_dict = json.loads(data)
     
        peer_id = addr[0] + ':' + str(addr[1])
        
        #si aun no existe este peer, entonces crearlo
        if peer_id in self.peers:
            peer = self.peers[peer_id]
        else:            
            peer = Peer(ip=addr[0], port=addr[1])
            self.peers[peer_id] = peer
            
            
        #store in our way
        trans = peer.recv(data_dict)
        
        #ya se recibieron todos los paquetes?
        if len(trans.packets) == data_dict['tp']:
            
            assembled_packet = self.assemble_packets(trans)
            
            
            #try to decrypt ... TO-DO: implement encription at send and recv
            
            #transmission complete, analize the message
            
            #self.analize_message(sock, data, addr)
            
            #data = json.loads(assembled_packet)
            
            '''
            if data['data'] != None:
                data_ok = data['data'].encode('utf8')
            else:
                data_ok = None
            
            data = {'msg':data['msg'].encode('utf8'), 'data':data_ok}
            print 'Message: ', data['msg']
            '''
            
            self.dispatch_message(assembled_packet, addr)
            
            #avisar que esta transmission ya llego completa
            #tosend = json.dumps({'msg':''})
            #self.sock.send(addr, )
            
    def assemble_packets(self, transmission):
        '''
        Reensambla todos los paquetes de una transmission y devuelve los datos como cadena de texto
        '''
        #print 'Ensamblando ' + str(len(transmission.packets)) + ' paquetes'
        
        s_out = ''
        for i in range(0, len(transmission.packets)):
            s_out += base64.b64decode(transmission.packets[i])
            
        return s_out
    
class NetgetSocket:
    '''
    Representa un socket con sus inputs y outputs
    '''
    def __init__(self, **kwargs):
        self.ip = kwargs.get('ip')
        self.port = kwargs.get('port', netget_port)
        self.addr = (self.ip, self.port)
        
        self.dispatcher = kwargs.get('dispatcher')
        
        
        # create the UDP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(self.addr)
        
        self.ngout = NetworkOut(sock=self.sock)
        self.ngin = NetworkIn(sock=self.sock, dispatch_message=self.incoming_message, ngout=self.ngout)
                
        
    def ping(self, w):
        self.ngout.netget_send((self.txt_ip.text.split(':')[0], int(self.txt_ip.text.split(':')[1]) ), self.txt_msg.text, self.txt_data.text)
        
    def incoming_message(self, data, addr):
        '''
        This message is analized and pass to Network if is necessary
        '''
        self.dispatcher(data, addr)
        
    def on_dismiss(self):
        self.__del__()
        
    def __del__(self):
        
        print 'Finalizando sockets'

        self.ngin.recv_thread.shutdown()

        #send packet to myself saying that must shutdown receiver
        self.ngout.netget_send(self.addr, 'shutdown')
        
        self.ngout.send_thread.shutdown()
        

class Network:
    '''
    - Wifi configurator
    - Ethernet configurator
    '''
    
    #state = StringProperty('offline')
    
    def __init__(self, **kwargs):
        
        self.on_netget_incoming = kwargs.get('on_netget_incoming')
        self.netget_sockets = []
        
    def has_connection(self):
        if len(self.netget_sockets) == 0:
            return False
            
        return True
                
    def discover_ips(self):
        
        try: #try unix
            ips = self.discover_ips_unix()
            print 'Unix IP solved'
        except:
            try:
                ips = self.discover_ips_android()
                print 'Android IP solved'
            except:
                #try windows
                ips = self.discover_ips_windows()
                print 'Windows IP solved'
                            
        return ips
                
    def discover_ips_android(self):
        
        texto = check_output('netcfg')
        
        ips = []
        
        for i in texto.split('\n'):
            if 'wlan0' in i:
                ip = i[43:].split('/')[0]
                print 'Salida android: '
                print ip
                ips.append(ip)
        
        return ips
        
    def discover_ips_unix(self):
        '''
        Seleccion de Ip con sistema operativo Unix y para Mac. Parche Netifaces
        '''
        ips = []
        
        texto = check_output('ifconfig')
        
        if texto == '':
            raise
        
        for i in texto.split('\n'):
            
            #MAC
            if "\tinet " in i:
                ip = i.split()[1] 
                if ip != "127.0.0.1":
                    ips.append( ip )
            #LINUX
            elif "Direc. inet:" in i:
                ip = i[22:].split()[0] 
                if ip != "127.0.0.1":
                    ips.append( ip )
            #linux raspberry
            elif "inet addr:" in i:
                ip = i[20:].split()[0] 
                if ip != "127.0.0.1":
                    ips.append( ip )
                    
        return ips
        
    def discover_ips_windows(self):
        
        ips = []
        
        texto = check_output('ipconfig')

        for i in texto.split('\n'):
            
            if 'Direcci' in i:
                ip = i[44:].split()[0] 
                if ip != "127.0.0.1":
                    ips.append( ip )
                    
        return ips

            
    def analize_message(self, data, addr):
        
        return
        
        print 'Analize message: ' + data['msg']
        
        #first we process the message in network level

        if data['msg'] == 'handshake_init':
            self.ngsock.ngout.netget_send(addr, 'handshake_init_ack', str(addr) )    #send not encrypted
            self.on_netget_incoming(data, addr)
        
        elif data['msg'] == 'handshake_init_ack':
            MessageBoxTime(msg='HANDSHAKE WITH SERVER CORRECT').open()
            self.state = 'ready'
            
        elif data['msg'] == 'solve_udp_info':
            self.sock.sendto('udp_info: ['+ addr[0] + ":" + str(addr[1]) + "]", addr)
        #elif data['msg'] == 'login':
        #    self.server_login(data['data'], addr)
        elif data['msg'] == 'login_ok':
            self.consola.text += "Login correcto"
            self.state = 'online'
            
        else:
            self.on_netget_incoming(data, addr)
            
    def host_discover(self):
            
        for sock in self.netget_sockets:
            
            baseip = sock.ip[:sock.ip.rfind('.')]
                
            for i in range(2, 255):
                
                ip = baseip + '.' + str(i)
                
                tosend = json.dumps({'msg':'ping', 'data':None})
                
                sock.ngout.send((ip, netget_port), tosend)
                
                
    def create_connection(self, dispatcher):
        '''
        Intenta obtener una conexion valida. Util cuando solo se dispone de una conexion
        
        Nota: Usa forsozamente el puerto 31415
        '''
        ips = self.discover_ips()

        if len(ips) >= 0:
            try:
                self.create_socket(ips[0], netget_port, dispatcher)
            except:
                try:
                    self.create_socket(ips[0], netget_port+1, dispatcher)
                except:
                    self.create_socket(ips[0], netget_port+2, dispatcher)
            return True
            
        return False
        
    def create_socket(self, ip, port=netget_port, dispatch_func=None):
        ngsock = NetgetSocket(ip=ip, port=port, dispatcher=dispatch_func)
        self.netget_sockets.append(ngsock)
     
    def send(self, addr, data):
        '''
        Try to send a packet on the first connected socket
        '''
        for i in self.netget_sockets:
            i.ngout.send(addr, data)
        
    def shutdown_network(self):
        for i in self.netget_sockets:
            i.__del__()
    
if __name__ == '__main__':
    
    
    net = Network()
    
    ip = net.discover_ips()[0]
    
    net.create_socket(ip, 1234)
    
    net.send((ip, 1234), 'Hola'*200)
    
    print "Terminado"
    
    net.shutdown_network()
    
    sleep(1)
    

    
