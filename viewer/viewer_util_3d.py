from pyglet.gl import *
from OpenGL.GLU import *
RAD2DEG = 57.29577951308232

def shape3D(v, h, c):
    if len(v) < 3:
        raise Exception("number of vertices must be bigger than 3.")
    if len(v) == 3:
        glBegin(GL_TRIANGLES)
    elif len(v) == 4:
        glBegin(GL_QUADS)
    else:
        glBegin(GL_POLYGON)
    glColor3f(c[0], c[1], c[2])
    for ver in v:
        glVertex3f(ver[0], ver[1], 0)
    glEnd()

    if len(v) == 3:
        glBegin(GL_TRIANGLES)
    elif len(v) == 4:
        glBegin(GL_QUADS)
    else:
        glBegin(GL_POLYGON)
    glColor3f(c[0], c[1], c[2])
    for ver in v:
        glVertex3f(ver[0], ver[1], h)
    glEnd()

    for i in range(len(v)):
        # side surfaces
        glBegin(GL_QUADS)
        glColor3f(c[0], c[1], c[2])
        glVertex3f(v[i][0], v[i][1], 0)
        glVertex3f(v[i][0], v[i][1], h)
        j = i+1
        if i == len(v)-1:
            j = 0
        glVertex3f(v[j][0], v[j][1], h)
        glVertex3f(v[j][0], v[j][1], 0)
        glEnd()

class Transform():
    #!!!!!
    def __init__(self):
        self.set_camera_point((0,0,1))
        self.set_target_point((0,0,0))
        self.set_direction((0,1,0))
        self.set_zoom(1)
        self.set_translate(0, 0, 0)
        self.set_ratio(1)

    def enable(self):
        glPushMatrix()
        glLoadIdentity()
        glTranslatef(*self.translate)
        gluPerspective(30, self.ratio, 0.1, 50.0)
        glScalef(self.zoom, self.zoom, self.zoom)
        gluLookAt(*(self.camera_point +
                  self.target_point +
                  self.direction))


    def disable(self):
        glPopMatrix()

    def set_camera_point(self, point):
        self.camera_point = point

    def set_target_point(self, point):
        self.target_point = point

    def set_direction(self, point):
        self.direction = point

    def set_zoom(self, zoom):
        self.zoom = zoom

    def set_translate(self, x, y, z):
        self.translate=(x, y, z)

    def set_ratio(self, r):
        self.ratio = r
