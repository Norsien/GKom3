import pygame
import numpy as np
from math import sqrt

#parameters
r = 144//2
WIDTH = 640*2
HEIGHT = 400*2
SIZE = r*2+1
color1 = np.array([162, 97, 161])
color2 = np.array([162, 97, 161])
color3 = np.array([255, 255, 255])
viewer = np.array([0, 0, 10])
ambi_const = 0.05
diff_const = 1
spec_const = 1
alpha = 100

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
sheet = pygame.Surface((SIZE, SIZE))

def pixel(surface, color, pos):
    color[color < 0] = 0
    color[color > 255] = 255
    color = np.rint(color)
    pcolor = pygame.Color(color)
    surface.fill(pcolor, (pos, (1, 1)))

def normalize(V):
    V = V / np.sqrt(np.sum(V**2))
    return V

def picture(poz):
    light = np.array(poz)
    shade = np.zeros((SIZE, SIZE, 3))
    for i in range(0, SIZE):
        for j in range(0, SIZE):
            x = (i-r)/r
            y = (j-r)/r
            if x**2 + y**2 <= 1:
                #ambient
                shade[i][j] += color1 * ambi_const

                #diffuse
                z2 = 1 - x**2 - y**2
                z = 0
                if z2 > 0:
                    z = sqrt(z2)
                N = normalize(np.array([x, y, z]))
                L = normalize(light - N)
                diffuse = max(0, np.dot(L, N))
                shade[i][j] += color2 * diffuse * diff_const

                #specular
                R = normalize(2 * diffuse * N - L)
                V = normalize(viewer - N)
                specular = max(0, np.dot(R, V))**alpha * spec_const
                shade[i][j] += color3 * specular
            pixel(sheet, shade[i][j], [i, j])
    screen.blit(sheet, ((WIDTH-SIZE)//2, (HEIGHT-SIZE)//2))

picture([-2, -2, 4])

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_press = pygame.mouse.get_pressed()
            if mouse_press[0]:
                org_poz = pygame.mouse.get_pos()
                x, y = org_poz
                x = 4 * (x - WIDTH//2) / r
                y = 4 * (y - HEIGHT//2) / r
                z = 4
                print(x, y, z)
                picture([x, y, z])
        if event.type == pygame.QUIT:
            running = False
    pygame.display.update()
pygame.quit()