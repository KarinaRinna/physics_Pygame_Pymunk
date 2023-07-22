import pygame as pg
from random import randrange
import pymunk.pygame_util
pymunk.pygame_util.positive_y_is_up = False


RES = WIDTH, HEGHT = 1200, 1000
FPS = 60

pg.init()
surface = pg.display.set_mode(RES)
clock = pg.time.Clock()
draw_oprions = pymunk.pygame_util.DrawOptions(surface)

space = pymunk.Space()
space.gravity = 0, 8000
ball_mass, ball_radius = 1, 7
segment_thickness = 6

a, b, c, d = 10, 100, 18, 40
x1, x2, x3, x4 = a, WIDTH // 2 - c, WIDTH // 2 +c, WIDTH - a
y1, y2, y3, y4, y5 = b, HEGHT // 4 -d, HEGHT // 4, HEGHT // 2 -1.5 * b, HEGHT - 4 * b
L1, L2, L3, L4 = (x1, -100), (x1, y1), (x2, y2), (x2, y3)
R1, R2, R3, R4 = (x4, -100), (x4, y1), (x3, y2), (x3, y3)
B1, B2 = (0, HEGHT), (WIDTH, HEGHT)


def create_ball(space, pos):
    ball_moment = pymunk.moment_for_circle(ball_mass, 0, ball_radius)
    ball_body = pymunk.Body(ball_mass, ball_moment)
    ball_body.position =pos
    ball_shape = pymunk.Circle(ball_body, ball_radius)
    ball_shape.elasticity = 0.1
    ball_shape.friction = 0.1
    space.add(ball_body, ball_shape)


def create_segment(from_, to_, thickness, space, color):
    segment_shape = pymunk.Segment(space.static_body, from_, to_, thickness)
    segment_shape.color = pg.color.THECOLORS[color]
    space.add(segment_shape)


def create_peg(x, y, space, color):
    circle_shape = pymunk.Circle(space.static_body, radius=10, offset=(x,y))
    circle_shape.color = pg.color.THECOLORS[color]
    circle_shape.elasticity = 0.1
    circle_shape.friction = 0.5
    space.add(circle_shape)


# pegs
peg_y, step = y4, 60
for i in range(10):
    peg_x = -1.5 * step if i % 2 else -step
    for j in range(WIDTH // step + 2):
        create_peg(peg_x, peg_y, space, 'darkslateblue')
        if i == 9:
            create_segment((peg_x, peg_y + 50), (peg_x, HEGHT), segment_thickness, space, 'darkslategray')
        peg_x += step
    peg_y += 0.5 * step

platforms = (L1, L2), (L2, L3),(L3, L4),(R1, R2), (R2, R3),(R3, R4)
for platform in platforms:
    create_segment(*platform, segment_thickness, space, 'darkolivegreen')
create_segment(B1, B2, 20, space, 'darkslategray')

while True:
    surface.fill(pg.Color('black'))

    for i in pg.event.get():
        if i.type == pg.QUIT:
            exit()
        if i.type == pg.MOUSEBUTTONDOWN:
            if i.button == 1:
                create_ball(space, i.pos)

    space.step(1 / FPS)
    space.debug_draw(draw_oprions)

    pg.display.flip()
    clock.tick(FPS)


# https://www.youtube.com/watch?v=rF1ra9xm9Pc