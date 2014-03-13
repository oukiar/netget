#!/usr/bin/python
# -*- coding: latin-1 -*-

from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stencilview import StencilView


from kivy.animation import Animation
from kivy.properties import NumericProperty

from widget3D import Widget3D, ZoomLayout3D

from kivy.graphics import *

class NatLines(Widget3D):
    
    def __init__(self, **kwargs):
        super(NatLines, self).__init__(**kwargs)
        
        self.color = kwargs.get('color')
        self.xsep = kwargs.get('xsep')
        self.ysize = kwargs.get('ysize')
        self.wline = kwargs.get('wline')

        with self.canvas:
            Color(self.color[0], self.color[1], self.color[2] ,1)
            self.draw_nat(self.xsep, self.ysize, self.wline)

      
    def draw_nat(self, xsep, ysize, linewidth=1):
        
        lowsep = .2
        #x = self.x
        x = 0
        #y = self.y
        y = 0
        
        Line(points=[x, y, 
                        x + xsep, y, 
                        x + xsep, y + ysize, 
                        x + xsep*2, y + ysize, 
                        x + xsep*2, y + ysize*lowsep,
                        ], width=linewidth)
                
                        
        #arc
        Line(points=self.arc(x + xsep*2.5, y + ysize*lowsep, -(xsep/2) , 20), width=linewidth)
        Line(points=self.arc(x + xsep*2.5, y + ysize*lowsep, xsep/2, 20), width=linewidth)
                        
        Line(points=[x + xsep*3, y + ysize*lowsep, x + xsep*3, y + ysize-ysize*lowsep], width=linewidth)
        
        
        #arc
        Line(points=self.invarc(x + xsep*3.5, y + ysize-ysize*lowsep, -(xsep/2), 20), width=linewidth)
        Line(points=self.invarc(x + xsep*3.5, y + ysize-ysize*lowsep, xsep/2, 20), width=linewidth)
            
                
        Line(points=[x + xsep*4, y + ysize-ysize*lowsep, x + xsep*4, y + ysize*lowsep], width=linewidth)
        
        #arc
        Line(points=self.arc(x + xsep*4.5, y + ysize*lowsep ,-(xsep/2), 20), width=linewidth)
        Line(points=self.arc(x + xsep*4.5, y + ysize*lowsep ,xsep/2, 20), width=linewidth)
                
        Line(points=[x + xsep*5, y + ysize*lowsep, x + xsep*5, y + ysize, x + xsep*6, y + ysize], width=linewidth)
        
                            
    def arc(self, x, y, r, steps):
        '''
        Circle without PI
        
        x = sqrt ( r² - y² )
        y = sqrt ( r² - x² )
        '''
        points = []
        
        for i in range(0, steps+1):
            x2 = r * (float(i)/steps)
            y2 = (r**2 - x2**2) ** .5
            points.append(x2+x)
            points.append(-y2+y)
            
        return points
        
    def invarc(self, x, y, r, steps):
        '''
        Circle without PI
        
        x = sqrt ( r² - y² )
        y = sqrt ( r² - x² )
        '''
        points = []
        
        for i in range(0, steps+1):
            x2 = r * (float(i)/steps)
            y2 = (r**2 - x2**2) ** .5
            points.append(x2+x)
            points.append(y2+y)
            
        return points



class NatLogo(Widget3D):
    
    lastpoint = NumericProperty(0)
    
    def __init__(self, **kwargs):
        super(NatLogo, self).__init__(**kwargs)
                
        self.size_logo = kwargs.get('size_logo')
                
        self.wline1 = 1.3
        self.wline2 = 1.1
        
        self.xsep = self.size_logo[0]/6
        self.ysize = self.size_logo[1]
                
        '''
        with self.canvas:
            Color(1,0,0,1)
            self.draw_nat(self.xsep, self.ysize, self.wline1)
            
            Color(.5,.5,.5,1)
            self.draw_nat(self.xsep, self.ysize, self.wline2)
        '''
        
        self.nat1 = NatLines(color=(.3,.3,1), 
                                xsep=self.xsep, 
                                ysize=self.ysize, 
                                wline=self.wline1, 
                                scale3D=(.5, .5, 1) )

        self.add_widget(self.nat1)
        
        self.nat2 = NatLines(color=(.5, .5, .5), 
                                xsep=self.xsep, 
                                ysize=self.ysize, 
                                wline=self.wline2, 
                                scale3D=(.5, .5, 1) )

        self.add_widget(self.nat2)

        #self.reanimate(None, 0)
        
    def animate(self):
        
        return
        
        self.canvas.clear()
        
        with self.canvas:
            Color(1,0,0,1)
            self.draw_nat(self.xsep, self.ysize, self.wline1)
            self.end_line1 = Line(points=[self.xsep*6, self.ysize, self.xsep*6, self.ysize], width=self.wline1)
            
            Color(.5,.5,.5,1)
            self.draw_nat(self.xsep, self.ysize, self.wline2)
            self.end_line2 = Line(points=[self.xsep*6, self.ysize, self.xsep*6, self.ysize], width=self.wline2)
            
        #init the line that complete the nat wave form
        self.lastpoint = self.ysize
        anim_lastpoint = Animation(lastpoint=0, duration=.5)
        anim_lastpoint.bind(on_complete=self.init_wave_move)
        anim_lastpoint.start(self)
        
    def on_lastpoint(self, w, val):
        self.end_line1.points = [self.x + self.xsep*6, self.y + self.ysize, self.x + self.xsep*6, self.y + val]
        self.end_line2.points = [self.x + self.xsep*6, self.y + self.ysize, self.x + self.xsep*6, self.y + val]
        
    def init_wave_move(self, w, dt):
        print 'init wave'
        Animation(x=-self.width, duration=1).start(self)
        
        
    def reanimate(self, w, val):
        self.rotate_z = 0
        
        anim = Animation(rotate_z=360, duration=3)
        
        anim.bind(on_complete=self.reanimate)
        anim.start(self)
            
    def draw_nat(self, xsep, ysize, linewidth=1):
        
        lowsep = .2
        #x = self.x
        x = 0
        #y = self.y
        y = 0
        
        Line(points=[x, y, 
                        x + xsep, y, 
                        x + xsep, y + ysize, 
                        x + xsep*2, y + ysize, 
                        x + xsep*2, y + ysize*lowsep,
                        ], width=linewidth)
                
                        
        #arc
        Line(points=self.arc(x + xsep*2.5, y + ysize*lowsep, -(xsep/2) , 20), width=linewidth)
        Line(points=self.arc(x + xsep*2.5, y + ysize*lowsep, xsep/2, 20), width=linewidth)
                        
        Line(points=[x + xsep*3, y + ysize*lowsep, x + xsep*3, y + ysize-ysize*lowsep], width=linewidth)
        
        
        #arc
        Line(points=self.invarc(x + xsep*3.5, y + ysize-ysize*lowsep, -(xsep/2), 20), width=linewidth)
        Line(points=self.invarc(x + xsep*3.5, y + ysize-ysize*lowsep, xsep/2, 20), width=linewidth)
            
                
        Line(points=[x + xsep*4, y + ysize-ysize*lowsep, x + xsep*4, y + ysize*lowsep], width=linewidth)
        
        #arc
        Line(points=self.arc(x + xsep*4.5, y + ysize*lowsep ,-(xsep/2), 20), width=linewidth)
        Line(points=self.arc(x + xsep*4.5, y + ysize*lowsep ,xsep/2, 20), width=linewidth)
                
        Line(points=[x + xsep*5, y + ysize*lowsep, x + xsep*5, y + ysize, x + xsep*6, y + ysize], width=linewidth)
        
                            
    def arc(self, x, y, r, steps):
        '''
        Circle without PI
        
        x = sqrt ( r² - y² )
        y = sqrt ( r² - x² )
        '''
        points = []
        
        for i in range(0, steps+1):
            x2 = r * (float(i)/steps)
            y2 = (r**2 - x2**2) ** .5
            points.append(x2+x)
            points.append(-y2+y)
            
        return points
        
    def invarc(self, x, y, r, steps):
        '''
        Circle without PI
        
        x = sqrt ( r² - y² )
        y = sqrt ( r² - x² )
        '''
        points = []
        
        for i in range(0, steps+1):
            x2 = r * (float(i)/steps)
            y2 = (r**2 - x2**2) ** .5
            points.append(x2+x)
            points.append(y2+y)
            
        return points


if __name__ == '__main__':
    from kivy.base import runTouchApp
    
    lay = BoxLayout()
    '''
    lay_zoom = ZoomLayout3D()    
    lay_zoom.add_widget(NatLogo() )
    
    lay.add_widget(lay_zoom)
    '''
    runTouchApp(NatLogo())
    #runTouchApp(lay)
