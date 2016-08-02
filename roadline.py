from pyglet.gl import *


width = 1024
height = 768
# Direct OpenGL commands to this window.
window = pyglet.window.Window(width=width, height=height)

zoom = 1

def shape3D(v, h, c):
    if len(v) < 3:
        raise Exception("number of vertices must be bigger than 3.")
    if len(v) == 3:
        glBegin(GL_TRIANGLES)
    elif len(v) == 4:
        glBegin(GL_QUADS)
    else:
        glBegin(GL_POLYGON)
    glColor3f(1, 1, 1)
    for ver in v:
        glVertex3f(ver[0], ver[1], 0)
    glEnd()

    if len(v) == 3:
        glBegin(GL_TRIANGLES)
    elif len(v) == 4:
        glBegin(GL_QUADS)
    else:
        glBegin(GL_POLYGON)
    glColor3f(1, 1, 1)
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

vertices2d = [
    (0, 100),
    (100, 100),
    (201, 201),
    (0, 200)
]

camera_point = [0, 0, 1]
target_point = [0, 0, 0]
up_direction = [0, 1, 0]

def lines():
    glBegin(GL_LINES)
    glVertex3f(0, 1000, 0)
    glVertex3f(0, 0, 0)
    glVertex3f(5, 1000, 0)
    glVertex3f(5, 0, 0)
    glEnd()

def on_draw():
    # print "draw"
    glPushMatrix()
    glLoadIdentity()
    glTranslatef(width/2, height/2, 0)
    gluPerspective(30, (width/height), 0.1, 50.0)
    gluLookAt(*(camera_point + target_point + up_direction))
    shape3D(vertices2d, 10, (1, 1, 1))
    # lines()

    glPopMatrix()

@window.event
def on_resize(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(gl.GL_PROJECTION)
    glMatrixMode(gl.GL_MODELVIEW)
    # glTranslatef(width / 2, height / 2, 0)
    glPushMatrix()

@window.event
def on_close():
    window.close()

# def on_key_press(k, mod):
#     if k == pyglet.window.key.Z:
#         camera_point += 1
#     if k == pyglet.window.key.X and zoom > 2:
#         glScalef(0.5, 0.5, 0.5)


while True:
    window.clear()
    window.switch_to()
    window.dispatch_events()

    on_draw()
    window.flip()
