#!/usr/bin/python
# -*- coding: latin-1 -*-


from kivy.core.window import Window
from kivy.animation import Animation
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

from kivy.core.image import Image as CoreImage
from kivy.properties import StringProperty, ListProperty, NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.clock import Clock

from kivy.graphics.transformation import Matrix


from kivy.graphics.opengl import *
from kivy.graphics import *


from kivy.graphics import Mesh
from functools import partial
from math import cos, sin, pi

#class Space3D(Widget):
class Widget3D(Widget):
    '''
    Works in 3D world ... the class can be named Space3D?
    
    Must be child of another widget, if you use this as Main widget a pygame parachute will ocurr
    
    Warning: Dont use as main widget, instead add as a child of standar Widget
    
    Note: Very Very experimental
    '''

    r = NumericProperty(1)
    g = NumericProperty(1)
    b = NumericProperty(1)
    
    color3D = ReferenceListProperty(r, g, b)
    '''
    Color of this widget
    '''
        
    scale_x = NumericProperty(1)
    scale_y = NumericProperty(1)
    scale_z = NumericProperty(1)
    
    scale3D = ReferenceListProperty(scale_x, scale_y, scale_z)
    '''
    Scale this widget
    '''
    
    rotate_x = NumericProperty(0)
    rotate_y = NumericProperty(0)
    rotate_z = NumericProperty(0)
    
    rotate3D = ReferenceListProperty(rotate_x, rotate_y, rotate_z)
    '''
    Rotation in degrees
    '''
    
    pos_x = NumericProperty(0)
    pos_y = NumericProperty(0)
    pos_z = NumericProperty(-10)
    pos3D = ReferenceListProperty(pos_x, pos_y, pos_z)
    '''
    Position on 3D space, please be carefull because (0,0,0) is not visible by the observer (Z=-15 is good)
    '''
    
    def __init__(self, **kwargs):
        self.scale3D = kwargs.pop('scale3D', (1,1,1))   #real size by default
        self.rotate3D = kwargs.pop('rotate3D', (0,0,0))
        self.pos3D = kwargs.pop('pos3D', (0,0,-15))     #z = -15 is good for the observer (person front of the monitor-screen-display-etc)

        #
        self.canvas = RenderContext(compute_normal_mat=True)

        #
        with self.canvas.before:
            self.cb_setup = Callback(self.setup_gl_context)
            PushMatrix()    #save the current opengl state
            #translate
            self.translate = Translate(self.pos_x, self.pos_y, self.pos_z)
            #rotate
            self._rotatex = Rotate(angle=self.rotate_x, axis=(1, 0, 0) )
            self._rotatey = Rotate(angle=self.rotate_y, axis=(0, 1, 0) )
            self._rotatez = Rotate(angle=self.rotate_z, axis=(0, 0, 1) )
            #scale
            self.scale = Scale(self.scale_x, self.scale_y, self.scale_z)
            
            self.cb_reset = Callback(self.reset_gl_context)
            
        with self.canvas:
            '''
            This widget have not canvas yet, please add your own canvas primitives in your derived class
            '''
            pass
            
        with self.canvas.after:
            #UpdateNormalMatrix()
            PopMatrix() #restore the previous opengl state 
          
        #configure 3D
        self.setup3D()
        
        super(Widget3D, self).__init__(**kwargs)
        
    def setup3D(self):
        asp = Window.width / float(Window.height)
        #self.canvas['projection_mat'] = Matrix().view_clip(-asp, asp, -1, 1, 1, 100, 1)
        self.canvas['projection_mat'] = Matrix().view_clip(-asp, asp, -1, 1, 1, 100, 1)
        
    
    #This version lacks of herencia 3D ... I think
    def add_widget(self, w, position=0):
        #only position is accumulative ... be carefull        
        w.pos_x += self.pos_x
        w.pos_y += self.pos_y
        w.pos_z += self.pos_z
        
        super(Widget3D, self).add_widget(w, position)
    
    def to2d(self):
        '''
        Return center and size 
        '''
    

    def on_rotate3D(self, w, val):
        '''
        Update rotation values for the canvas draws, ... bad performance here? (float/float)
        '''
        self.setup3D()
        self._rotatex.angle = val[0]
        self._rotatey.angle = val[1]
        self._rotatez.angle = val[2]
        
    def on_pos3D(self, w, val):
        self.translate.x = val[0]
        self.translate.y = val[1]
        self.translate.z = val[2]
        
        for i in self.children:
            i.pos3D = self.pos3D
        
    def on_scale3D(self, w, val):
        
        self.scale.x = val[0]
        self.scale.y = val[1]
        self.scale.z = val[2]
        
        #changue all out childreen scale too ... be carefull, this is equal on childs and parents
        for i in self.children:
            i.scale3D = self.scale3D
    
    '''       
    def on_opacity(self, w, val):
        for i in self.children:
            i.opacity = val
    '''
    
    def setup_gl_context(self, *args):
        glEnable(GL_DEPTH_TEST)

    def reset_gl_context(self, *args):
        glDisable(GL_DEPTH_TEST)
        
class ZoomLayout3D(Widget3D):
    '''
    Layout that lets you make zoom in the scene
    
    By the moment, only change the scale of them childrens
    '''
    def __init__(self, **kwargs):
        super(ZoomLayout3D, self).__init__(**kwargs)
        
    def add_widget(self, widget, index=0):
        super(ZoomLayout3D, self).add_widget(widget, index)
        
    def on_touch_down(self, touch):

        if touch.button == 'scrolldown':
            print('Zoom in')
            
            for i in self.children:
                i.scale_x +=.1
                i.scale_y +=.1
            
        elif touch.button == 'scrollup':
            print('Zoom out')
            
            for i in self.children:
                i.scale_x -=.1
                i.scale_y -=.1
            
        super(ZoomLayout3D, self).on_touch_down(touch)
        
class Slider3D(Widget3D):
    pass

class Pivot3D(Widget3D):
    pass
        
class Image3D(Widget3D):
    texture = ObjectProperty()
    
    def __init__(self, **kwargs):
        super(Image3D, self).__init__(**kwargs)
        self.texture = CoreImage(kwargs.get('source')).texture
        with self.canvas:
            Rectangle(texture=self.texture, pos=(-5, -5), size=(10,10))
            
    def on_texture(self, text, val):
        self.canvas.clear()
        with self.canvas:
            #Color(1,1,1,self.opacity)
            
            Rectangle(texture=self.texture, pos=(-5, -5), size=(10,10))
    
        #self.canvas.opacity = .3
    
class Video3D(Widget3D):
    
    def __init__(self, **kwargs):
        super(Video3D, self).__init__(**kwargs)
        self.source = kwargs.get('source', None)
        
        if self.source != None:
            self._video = Video(source=self.source)
            
            self.add_widget(self._video)
       
class rotatingImage(Image3D):
    def __init__(self, **kwargs):
        super(rotatingImage, self).__init__(**kwargs)
        self.reanimate(None, 0)   
        
    def reanimate(self, w, val):
        self.rotate_z = 0
        
        anim = Animation(rotate_z=360, duration=3)
        
        anim.bind(on_complete=self.reanimate)
        anim.start(self)
        
class rotatingPoints(Widget3D):
    '''
    Example of make 3D points animation (based on 3Drendering and canvas/mesh examples)
    '''
    
    
    r = NumericProperty(1)
    g = NumericProperty(1)
    b = NumericProperty(1)
    
    color3D = ReferenceListProperty(r, g, b)
    '''
    Color of this widget
    '''
    
    def __init__(self, **kwargs):
        
        super(rotatingPoints, self).__init__(**kwargs)
        
        self.color3D = kwargs.get('color', (1, 1, 1))
        
        #you only need draw in 3D
        with self.canvas:
            self.color = Color(self.r, self.g, self.b)
            self.mesh = self.build_mesh()
            
        self.reanimate(None, 0)
            
    def build_mesh(self):
        vertices = []
        indices = []
        step = 10
        istep = (pi * 2) / float(step)
        xpos = 0
        ypos = 0
        for i in range(step):
            x = xpos + cos(istep * i) * 1
            y = ypos + sin(istep * i) * 1
            #vertices.extend([x, y, 0, 0])
            vertices.extend([x, y])
            indices.append(i)
            
        return Point(points=vertices, pointsize=2)
        return Line(points=vertices)
        #return Mesh(vertices=vertices, indices=indices, mode='points', pointsize=4)
        
        
        
    def reanimate(self, w, val):
        self.rotate_y = 0
        self.rotate_z = 0
        
        anim = Animation(rotate_z=360, duration=3)
        #anim = Animation(rotate_y=360, rotate_z=360, duration=3)
        
        anim.bind(on_complete=self.reanimate)
        anim.start(self)
        
class Circle(Widget3D):
    '''
    Circle without PI
    
    x = sqrt ( r² - y² )
    y = sqrt ( r² - x² )
    '''
    
    def __init__(**kwargs):
        super(Circle, self).__init__(**kwargs)
        
        self.radius = 5
    
def main():
    
    return rotatingPoints(size_hint=(None,None), size=(10,10), pos3D=(0,0,-15), rotate3D=(0,0,0) )
        
if __name__ == '__main__':
    from kivy.base import runTouchApp
    from kivy.uix.video import Video
    import sys
    
    #runTouchApp( Widget3D( pos3D=(0,0,-15), rotate3D=(0,45,0) ) )
    #runTouchApp( rotatingPoints( pos3D=(0,0,-15), rotate3D=(0,0,0) ) )
    
    lay = BoxLayout()
    #lay.add_widget(Image3D(source='default.png', pos3D=(0,0,-10)))
    #lay.add_widget(Button(text='bnada'))
    #lay.add_widget(rotatingPoints(size_hint=(None,None), size=(10,10), pos3D=(0,0,-15), rotate3D=(0,0,0) ))
    
    #lay.add_widget(rotatingImage(source='cover.png', pos3D=(17.5,-6,-20)) )
    
    #lay.add_widget(LoginLogo( pos3D=(0,0,-5) ) )
    
    lay_zoom = ZoomLayout3D()
    
    lay_zoom.add_widget(NatLogo() )
    #lay_zoom.add_widget(Video3D(source=sys.argv[1]) )
    
    lay.add_widget(lay_zoom)
    
    runTouchApp(lay)
    #runTouchApp(NatLogo() )
    
    
