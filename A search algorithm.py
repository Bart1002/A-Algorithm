## ----------------------- SETTINGS ----------------------- ##
# left mouse button + :
# LCTRL -> start
# RCTRL -> stop
# no key -> obstacle
# colors:
# intense blue - the node was taken into consideration during finding the path
# light blue - the node wasn't taken into consideration during finding the path
# red - start
# purple - stop
# gray - obstacle

import pygame
import math
pygame.init()

win = pygame.display.set_mode((710, 710))

pygame.display.set_caption("Game")


class Node:
    staticLength = 40

    def __init__(self, _x, _y, neighbours):
        self.x = _x
        self.y = _y
        self.start = False
        self.stop = False
        self.obstacle = False
        self.visited = False
        self.neighbours = neighbours
        self.parent = -1
        self.global_goal = 1000000
        self.local_goal = 1000000


def return_color(i):
    if i.start:
        return [255, 0, 0]
    if i.stop:
        return [153, 0, 255]
    if i.obstacle:
        return [82, 82, 122]
    if i.visited == False:
        return [135, 206, 250]

    return [51, 133, 255]


nodes = []

# creating nodes
for y in range(0, 14):
    for x in range(0, 14):
        neighbours = []
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                if i < 0 or j < 0 or i > 14 - 1 or j > 14 - 1 or (i == x and j == y):
                    continue
                neighbours.append(i + j * 14)

        nodes.append(Node(x * 40 + (x + 1) * 10, y *
                          40 + (y + 1) * 10, neighbours))

if_start = [True, 0, 13]
if_stop = [True, 13, 0]
nodes[13 * 14].start = True
nodes[13].stop = True

# draw


def draw_path():
    current = nodes[if_stop[1] + if_stop[2] * 14]

    while current.parent != -1:
        parent = nodes[current.parent]
        pygame.draw.line(win, (255, 215, 0), (current.x + 20,
                                              current.y + 20), (parent.x + 20, parent.y + 20), 3)
        pygame.display.update()
        current = parent


def draw_board():
    win.fill((0, 0, 0))  # clear screen

    for i in nodes:  # draw nodes
        pygame.draw.rect(win, return_color(
            i), (i.x, i.y, i.staticLength, i.staticLength))
    pygame.display.update()

    if nodes[if_stop[1] + if_stop[2] * 14].parent != -1:
            draw_path()


run = True


def Find_Path():
    def heuristic(current, stop): return int(math.sqrt(math.pow(math.fabs(
        current.x - stop.x), 2) + math.pow(math.fabs(current.y - stop.y), 2)))

    # clear nodes
    for i in nodes:
        i.visited = False
        i.parent = -1
        i.global_goal = 1000000
        i.local_goal = 1000000

    nodes[if_start[1] + if_start[2] * 14].local_goal = 0
    nodes[if_start[1] + if_start[2] * 14].global_goal = heuristic(
        nodes[if_start[1] + if_start[2] * 14], nodes[if_stop[1] + if_stop[2] * 14])

    to_check = []
    to_check.append(if_start[1] + if_start[2] * 14)

    while len(to_check) > 0 and nodes[if_stop[1] + if_stop[2] * 14].parent == -1:
        while nodes[to_check[0]].visited:
            to_check.pop(0)
            if len(to_check) == 0:
                break
        if len(to_check) == 0:
                break
        for i in nodes[to_check[0]].neighbours:
            if nodes[i].obstacle:
                continue

            if nodes[i].local_goal > nodes[to_check[0]].local_goal + heuristic(nodes[i], nodes[to_check[0]]):
                nodes[i].parent = to_check[0]
                nodes[i].local_goal = nodes[to_check[0]].local_goal + \
                    heuristic(nodes[i], nodes[to_check[0]])
                nodes[i].global_goal = heuristic(
                    nodes[i], nodes[if_stop[1] + if_stop[2] * 14]) + nodes[i].local_goal
            if nodes[i].stop:
                continue
            if nodes[i].visited == False:
                to_check.append(i)

        nodes[to_check[0]].visited = True
        to_check.pop(0)
        to_check.sort(key=lambda i: nodes[i].global_goal)


Find_Path()
draw_board()

while run:

    pygame.time.delay(100)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    if_change = False

    if pygame.mouse.get_pressed()[0]:
        keys = pygame.key.get_pressed()

        x, y = pygame.mouse.get_pos()

        if (x < 20 or y < 20):
             continue

        x -= 10
        y -= 10
        x /= 50
        y /= 50

        x = int(x)
        y = int(y)

        while True:
            if keys[pygame.K_LCTRL]:  # LCTRL -> start

                nodes[if_start[1] + if_start[2] * 14].start = False
                nodes[x + y * 14].stop = False
                nodes[x + y * 14].obstacle = False
                if_start[1] = x
                if_start[2] = y
                nodes[x + y * 14].start = True
                if_change = True

                break

            if keys[pygame.K_RCTRL]:  # RCTRL -> stop

                nodes[if_stop[1] + if_stop[2] * 14].stop = False
                nodes[x + y * 14].stop = True
                nodes[x + y * 14].obstacle = False
                if_stop[1] = x
                if_stop[2] = y
                nodes[x + y * 14].start = False
                if_change = True

                break

            # no key -> obstacle
            if nodes[x + y * 14].start or nodes[x + y * 14].stop:
                break

            if nodes[x + y * 14].obstacle:
                nodes[x + y * 14].obstacle = False
                if_change = True
                break

            nodes[x + y * 14].obstacle = True
            if_change = True
            break

    if if_change:
        Find_Path()
        draw_board()
