import pygame
import numpy as np


W_SIZE = WIDTH, HEIGHT = 1400, 1000
H_WIDTH, H_HEIGHT = WIDTH // 2, HEIGHT // 2
screen = pygame.display.set_mode(W_SIZE)
display = pygame.Surface(W_SIZE)
selection = pygame.Surface(W_SIZE)
selection.set_colorkey((0, 0, 0))
clock = pygame.time.Clock()
FPS = 60

iterations = 255
size = 1000
h_size = size // 2


def complex_matrix(xmin, xmax, ymin, ymax, pixel_density):
    re = np.linspace(xmin, xmax, pixel_density)
    im = np.linspace(ymin, ymax, pixel_density)
    return re[np.newaxis, :] + im[:, np.newaxis] * 1j


def get_escape_iterations(c, num_iterations):
    colors = np.zeros((size, size))
    z = 0
    for i in range(1, num_iterations + 1):
        z = z**2 + c
        mask = (colors == 0) & (abs(z) > 2)
        colors[mask] = i
    mask = (colors == 0) & (abs(z) < 2)
    colors[mask] = iterations
    return colors


def draw(x1=-2, y1=-2, dd=4):
    c = complex_matrix(x1, x1 + dd, y1, y1 + dd, pixel_density=size)
    iteration = get_escape_iterations(c, num_iterations=iterations)
    colors = iteration / iterations * 230
    colors = colors.T

    rgb_arr = np.repeat(colors[..., np.newaxis], 3, axis=2)
    rgb_arr = rgb_arr.astype(np.uint8)
    surface = pygame.surfarray.make_surface(rgb_arr)

    display.fill((0, 0, 0))
    display.blit(surface, (H_WIDTH - size // 2, H_HEIGHT - size // 2))


draw()
smx, smy = None, None
current_state = [-2, -2, 4]

clicked = False
while True:
    screen.fill((0, 0, 0))
    selection.fill((0, 0, 0))

    mx, my = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                draw()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                x, y = mx - H_WIDTH, my - H_HEIGHT
                rel_start = ((x + h_size) / size, (y + h_size) / size)

                x = current_state[2] * x / size
                y = current_state[2] * y / size

                start_drag = x, y
                smx, smy = mx, my
                clicked = True

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                x, y = mx - H_WIDTH, my - H_HEIGHT
                x = current_state[2] * x / size
                y = current_state[2] * y / size

                dd = max(abs(start_drag[0] - x), abs(start_drag[1] - y))

                left = current_state[0] + rel_start[0] * current_state[2]
                top = current_state[1] + rel_start[1] * current_state[2]

                current_state = left, top, dd
                draw(left, top, dd)
                clicked = False

    if clicked:
        pygame.draw.rect(selection, (1, 1, 1), (smx, smy,
                         *(max(abs(smx - mx), abs(smy - my)),) * 2), 2)
        pygame.draw.rect(selection, (255, 255, 255), (smx, smy,
                         *(max(abs(smx - mx), abs(smy - my)),) * 2), 1)

    screen.blit(display, (0, 0))
    screen.blit(selection, (0, 0))
    pygame.display.update()
    clock.tick(FPS)
