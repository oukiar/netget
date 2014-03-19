#!/usr/bin/python
# -*- coding: latin-1 -*-

from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.colorpicker import ColorPicker
from kivy.uix.slider import Slider
from kivy.uix.scatterlayout import ScatterLayout
from kivy.uix.popup import Popup


from kivy.graphics import *

class NatLines(Widget):
    
    def __init__(self, **kwargs):
        super(NatLines, self).__init__(**kwargs)
        
        self.color1 = kwargs.get('color1')
        self.color2 = kwargs.get('color2')
        self.xsep = self.width/6 
        self.ysize = self.height
        self.wline1 = kwargs.get('wline1')
        self.wline2 = kwargs.get('wline2')
            
        self.mydraw()
            
    def mydraw(self):
        
        print 'drawcolor1', self.color1
        print 'drawcolor2', self.color2
        
        #determinar cual linea es mas gruesa
        if self.wline1 > self.wline2:
            self.majorline = self.wline1
        else:
            self.majorline = self.wline2
            
        self.canvas.clear()
        
        if hasattr(self, 'fbo'):
            self.fbo.clear()

        with self.canvas:
            self.fbo = Fbo(size=(self.width+(self.majorline*2), (self.height+self.majorline*2) ) )
            Rectangle(size=self.size, texture=self.fbo.texture)
        
        
        with self.fbo:
            Color(self.color1[0], self.color1[1], self.color1[2] ,1)
            self.draw_nat(self.xsep, self.ysize, self.wline1)
            
            Color(self.color2[0], self.color2[1], self.color2[2] ,1)
            self.draw_nat(self.xsep, self.ysize, self.wline2)

    def save(self, filename):
        self.fbo.texture.save(filename)
        
    def draw_nat(self, xsep, ysize, linewidth=1):
        
        steps = 20
        lowsep = .15
        x = self.x + self.majorline
        y = self.y + self.majorline
        
        Line(points=[x, y, 
                        x + xsep, y, 
                        x + xsep, y + ysize, 
                        x + xsep*2, y + ysize, 
                        x + xsep*2, y + ysize*lowsep,
                        ], width=linewidth)
                
                        
        #arc
        Line(points=self.arc(x + xsep*2.5, y + ysize*lowsep, -(xsep/2) , steps, -1), width=linewidth)
        Line(points=self.arc(x + xsep*2.5, y + ysize*lowsep, xsep/2, steps, -1), width=linewidth)
                        
        Line(points=[x + xsep*3, y + ysize*lowsep, x + xsep*3, y + ysize-ysize*lowsep], width=linewidth)
        
        
        #arc
        Line(points=self.arc(x + xsep*3.5, y + ysize-ysize*lowsep, -(xsep/2), steps, 1), width=linewidth)
        Line(points=self.arc(x + xsep*3.5, y + ysize-ysize*lowsep, xsep/2, steps, 1), width=linewidth)
            
                
        Line(points=[x + xsep*4, y + ysize-ysize*lowsep, x + xsep*4, y + ysize*lowsep], width=linewidth)
        
        #arc
        Line(points=self.arc(x + xsep*4.5, y + ysize*lowsep ,-(xsep/2), steps, -1), width=linewidth)
        Line(points=self.arc(x + xsep*4.5, y + ysize*lowsep ,xsep/2, steps, -1), width=linewidth)
                
        Line(points=[x + xsep*5, y + ysize*lowsep, x + xsep*5, y + ysize, x + xsep*6, y + ysize], width=linewidth)
        
                            
    def arc(self, x, y, r, steps, updir):
        '''
        Points of arc calculated without PI or trigonometry maths
        
        Ecuations for calculate points of circle
        x = sqrt ( r² - y² )
        y = sqrt ( r² - x² )
        '''
        points = []
        
        for i in range(0, steps+1):
            x2 = r * (float(i)/steps)
            y2 = (r**2 - x2**2) ** .5
            points.append(x2+x)
            points.append((y2*updir)+y)
            
        return points

class NatLogo(FloatLayout):
    
    def __init__(self, **kwargs):
        super(NatLogo, self).__init__(**kwargs)
        
        self.nat = NatLines(size=(500,300), 
                                color1=(1,1,1), wline1=8,
                                color2=(0,0,1), wline2=3
                                )
                                
        self.add_widget(self.nat)
        
        
        #layout superior de controles
        self.lay_upper = AnchorLayout(anchor_x='center', anchor_y='top')
        
        self.layout = BoxLayout(orientation='vertical', size_hint=(None,None), size=(300,400), opacity=.8)
        

        #SELECCION DE COLOR
        self.cp_color = ColorPicker(size_hint_y=5)
        
        self.btn_line1 = Button(text='Color Linea 1', on_press=self.configcolor1)
        self.sld_line1 = Slider(value=8, min=1, max=20)
        self.sld_line1.bind(value=self.on_wline1)
        
        self.btn_line2 = Button(text='Color Linea 2', on_press=self.configcolor2)
        self.sld_line2 = Slider(value=3, min=1, max=10)
        self.sld_line2.bind(value=self.on_wline2)
        
        
        self.btn_save = Button(text='Guardar logotipo', on_press=self.save_natlogo)
        
        self.layout.add_widget(self.btn_line1)
        self.layout.add_widget(self.sld_line1)
        self.layout.add_widget(self.btn_line2)
        self.layout.add_widget(self.sld_line2)
        self.layout.add_widget(self.btn_save)
        self.layout.add_widget(self.cp_color)
        
        self.lay_upper.add_widget(self.layout)
        self.add_widget(self.lay_upper)
        
    def configcolor1(self, w):
        self.nat.color1 = self.cp_color.color
        print 'color 1', self.nat.color1
        print 'color 2', self.nat.color2
        self.nat.mydraw()
        
    def configcolor2(self, w):
        self.nat.color2 = self.cp_color.color
        print '2color 1', self.nat.color1
        print '2color 2', self.nat.color2
        self.nat.mydraw()
        
    def save_natlogo(self, w):
        self.nat.save('nat-logo.png')
        
    def on_wline1(self, w, val):
        self.nat.wline1 = val
        self.nat.mydraw()

    def on_wline2(self, w, val):
        self.nat.wline2 = val
        self.nat.mydraw()
        
if __name__ == '__main__':
    from kivy.base import runTouchApp
    from kivy.core.window import Window
    
    runTouchApp(NatLogo())
