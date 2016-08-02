import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import random


vertices = (
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, -1, 1),
    (-1, 1, 1)
)

edges = (
    (0, 1),
    (0, 3),
    (0, 4),
    (2, 1),
    (2, 3),
    (2, 7),
    (6, 3),
    (6, 4),
    (6, 7),
    (5, 1),
    (5, 4),
    (5, 7)
)

surfaces = (
    (0, 1, 2, 3),
    (3, 2, 7, 6),
    (6, 7, 5, 4),
    (4, 5, 1, 0),
    (1, 5, 7, 2),
    (4, 0, 3, 6)
)

colors = (
    (1, 0, 0),
    (0, 1, 0),
    (0, 0, 1),
    (0, 1, 0),
    (1, 1, 1),
    (0, 1, 1),
    (1, 0, 0),
    (0, 1, 0),
    (0, 0, 1),
    (1, 0, 0),
    (1, 1, 1),
    (0, 1, 1),
)

ground_surfaces = (0, 1, 2, 3)

ground_vertices = (
    (-10, -0.1, 50),
    (10, -0.1, 50),
    (-10, -0.1, -300),
    (10, -0.1, -300),

)


def Ground():
    glBegin(GL_QUADS)

    x = 0
    for vertex in ground_vertices:
        x += 1
        glColor3fv((0, 1, 1))
        glVertex3fv(vertex)

    glEnd()


def Cube():
    glBegin(GL_QUADS)

    for surface in surfaces:
        x=0
        for vertex in surface:
            x += 1
            glColor3fv(colors[x])
            glVertex3fv(vertices[vertex])

    glEnd()

    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()


def set_vertices(max_distance, min_distance=-20, camera_x=0, camera_y=0):
    camera_x = -1 * int(camera_x)
    camera_y = -1 * int(camera_y)

    x_value_change = random.randrange(camera_x - 75, camera_x + 75)
    y_value_change = random.randrange(camera_y - 75, camera_y + 75)

    z_value_change = random.randrange(-1 * max_distance, min_distance)

    new_vertices = []

    for vert in vertices:
        new_vert = []

        new_x = vert[0] + x_value_change
        new_y = vert[1] + y_value_change
        new_z = vert[2] + z_value_change

        new_vert.append(new_x)
        new_vert.append(new_y)
        new_vert.append(new_z)

        new_vertices.append(new_vert)

    return new_vertices


def Cubes(new_vertices):
    glBegin(GL_QUADS)

    for surface in surfaces:
        x = 0

        for vertex in surface:
            x += 1
            glColor3fv(colors[x])
            glVertex3fv(new_vertices[vertex])

    glEnd()


# CUT LINES BC THEY HURT PROCESSING
##    glBegin(GL_LINES)
##    for edge in edges:
##        for vertex in edge:
##            glVertex3fv(new_vertices[vertex])
##    glEnd()


def Shape3D(v, h, c):
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
        glColor3f(c[i][0], c[i][1], c[i][2])
        glVertex3f(v[i][0], v[i][1], 0)
        glVertex3f(v[i][0], v[i][1], h)
        j = i+1
        if i == len(v)-1:
            j = 0
        glVertex3f(v[j][0], v[j][1], h)
        glVertex3f(v[j][0], v[j][1], 0)
        glEnd()

vertices2d = [
    (-1, 0),
    (0, 0),
    (1, 1),
    (-1, 1)
]

def main():
    pygame.init()
    display = (800,600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)

    gluLookAt(0, 0, -20,
              0, 0, 0,
              0, 1, 0)
    # glTranslatef(0.0,0.0, -10)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # glRotatef(1, 3, 1, 1)
        # glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        Shape3D(vertices2d, 1, [[1,1,1]]*len(vertices2d))
        pygame.display.flip()
        pygame.time.wait(10)


main()