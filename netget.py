#!/usr/bin/python
# -*- coding: latin-1 -*-

from kivy.core.window import Window
from kivy.animation import Animation

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label

from kivy.graphics import *

from widget3D import Widget3D
from nat import NatLogo

class Login(BoxLayout):
    def __init__(self, **kwargs):
        super(Login, self).__init__(orientation='vertical', size_hint=(None,None), size=(300,140), center=Window.center, **kwargs)
        #little code fixbug
        self.center = Window.center
        
        self.txt_user = TextInput(text='Usuario')
        self.add_widget(self.txt_user)
        
        self.txt_pass = TextInput(text='Password')
        self.add_widget(self.txt_pass)
        
        self.btn_iniciar_sesion = Button(text='Iniciar sesión')
        self.add_widget(self.btn_iniciar_sesion)
        
class Netget(FloatLayout):
    def __init__(self, **kwargs):
        super(Netget, self).__init__(**kwargs)
        
        with self.canvas.before:
            Color(.9,.9,.9,1)
            Rectangle(size=Window.size)
        
        self.natlogo = NatLogo(pos_x=-6, pos_y=10, size_logo=(25,10) )
        self.add_widget(self.natlogo )
        
        self.login = Login()
        self.add_widget(self.login)
        
        #login bind
        self.login.btn_iniciar_sesion.bind(on_press=self.on_login)
        
    def on_login(self, w):
        Animation(opacity=0, duration=.3).start(self.login)
        
        anim_nat = Animation(pos_y=0, duration=.3)
        anim_nat.bind(on_complete=self.init_nat_animation)
        
        anim_nat.start(self.natlogo)
            
    def init_nat_animation(self, w, dt):
        pass
        #self.natlogo.animate()
            
if __name__ == '__main__':
    from kivy.base import runTouchApp

    runTouchApp(Netget() )
