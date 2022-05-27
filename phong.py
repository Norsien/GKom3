import pygame
import numpy as np
from math import sqrt

WIDTH = 640
HEIGHT = 400
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

def pixel(surface, color, pos):
    color[color < 0] = 0
    color[color > 255] = 255
    color = np.rint(color)
    pcolor = pygame.Color(color)
    surface.fill(pcolor, (pos, (1, 1)))

def normalize(V):
    V = V / np.sqrt(np.sum(V**2))
    return V

r = 144
SIZE = r*2+1
sheet = pygame.Surface((SIZE, SIZE))

shade = np.zeros((SIZE, SIZE, 3))
light = np.array([3, 15, 20])
viewer = np.array([0, 0, 20])

color = np.array([16, 10, 16])
color2 = np.array([255, 255, 255])

for i in range(0, SIZE):
    for j in range(0, SIZE):
        if ((i-r)/r) ** 2 + ((j-r)/r) ** 2 <= 1:
            #ambient
            shade[i][j] += color

            #diffuse
            x = (i-r)/r
            y = (j-r)/r
            z2 = 1 - x**2 - y**2
            z = 0
            if z2 > 0:
                z = sqrt(z2)
            N = normalize(np.array([x, y, z]))
            L = normalize(light - N)
            diffuse = np.dot(L, N)
            if i == 70 and j == 80:
                print(N, L)
            shade[i][j] += color * diffuse * 4

            #specular
            R = normalize(2 * diffuse * N - L)
            V = normalize(viewer - N)
            specular = np.dot(R, V)**10 * 0.2
            shade[i][j] += color2 * specular

for i in range(0, SIZE):
    for j in range(0, SIZE):
        pixel(sheet, shade[i][j], [i, j])

screen.blit(sheet, ((WIDTH-SIZE)//2, (HEIGHT-SIZE)//2))
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.update()
pygame.quit()