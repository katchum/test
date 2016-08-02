import pyglet
from pyglet.gl import *
import math

from viewer_util_3d import *

import numpy as np

WIDTH = 1024
HEIGHT = 768
ZOOM = 1.0



class Viewer():
    def __init__(self, type='omniscent'):
        self.type = type
        self.width = WIDTH  # width of the screen
        self.height = HEIGHT    # height of the screen
        self.window = pyglet.window.Window(width=self.width, height=self.height, display=None)  # pyglet window instance for rendering
        self.transform = Transform()    # transformation matrix for adjusting viewpoint
        self.window.on_close = self.close   # set the function callback when the window closes
        self.zoom = ZOOM    # set the zooming factor

        self.transform = Transform()
        self.transform.set_translate(self.width/2, self.height/2, 0)
        self.transform.set_ratio()
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        @self.window.event
        def on_resize(width,height):
            glViewport(0, 0, width, height)
            glMatrixMode(gl.GL_PROJECTION)
            glLoadIdentity()
            gluPerspective(60, width / float(height), -10000, 10000)
            glMatrixMode(gl.GL_MODELVIEW)
            glTranslatef(self.width / 2, self.height / 4, 0)
            glPushMatrix()

    def render(self, draw_list, camera_point, direction, html_info=''):
        """
        render the current timestep. called in dynamic's step function
        """

        # draw everything in the world and then set the center to the car.
        for shape in draw_list:
            self.draw_3d(shape)

        # set camera location
        self.transform.set_camera_point(camera_point)
        self.transform.set_target_point(direction)
        self.transform.set_zoom(self.get_zoom())
        # self.transform.set_target_point([loc[0] + dir[0], loc[1] + dir[1], -10])
        self.transform.set_direction([0, 0, 1])

        # render everything on the canvase
        self._render(html_info=html_info)

    def draw_3d(self, shape):
        for item in shape:
            color = [1, 1, 1]
            height = 0.1
            vertices = item["vertices"]
            if "color" in item:
                color = item["color"]
            if "height" in item:
                height = item["height"]
            self._draw_3d(vertices, height, color)

    def _draw_3d(self, v, h, c):
        self.geoms_3d.append([v, h, c])

    def set_key_reaction(self, on_key_press, on_key_release):
        """set the callback function for keyboard input"""
        def keypress(k, mod): # pack the general key press function together with the agent-specific key press function
            self.general_key_press(k, mod)
            on_key_press(k, mod)

        def keyrelease(k, mod): # pack the general key release function together with the agent-specific key release function
            self.general_key_release(k, mod)
            on_key_release(k, mod)
        self.window.on_key_press = keypress
        self.window.on_key_release = keyrelease

    def general_key_press(self, k, mod):
        if k == pyglet.window.key.Z:
            self.zoom_change(0.1)
        if k == pyglet.window.key.X:
            self.zoom_change(-0.1)


    def general_key_release(self, k, mod):
        pass

    def close(self):
        """
        close the viewer
        """
        self.window.close()

    def zoom_change(self, val):
        self.zoom += val
        print self.zoom

    def get_zoom(self):
        return math.exp(self.zoom)

    def _render(self, return_rgb_array=False, html_info=''):
        """
        clear the window and render all the things drawn earlier
        """
        glClearColor(0.3, 0.5, 0.2, 0.4)
        self.window.clear()
        self.window.switch_to()
        self.window.dispatch_events()
        self.transform.enable()
        for geom_3d in self.geoms_3d:
            shape3D(*geom_3d)
        self.transform.disable()
        arr = None
        self._draw_data(html_info)   # write the info the self.character
        self.window.flip()
        self.onetime_geoms = []
        self.geoms_3d = []
        return arr

    def _draw_data(self, html_info):
        """
        print the info of self.character on the screen
        """
        document = pyglet.text.decode_html(html_info)
        layout = pyglet.text.layout.TextLayout(document, 10000, self.window.height, multiline=True)
        layout.draw()

    def get_array(self):
        """not used
        """
        self.window.flip()
        image_data = pyglet.image.get_buffer_manager().get_color_buffer().get_image_data()
        self.window.flip()
        arr = np.fromstring(image_data.data, dtype=np.uint8, sep='')
        arr = arr.reshape(self.height, self.width, 4)
        return arr[::-1, :, 0:3]
