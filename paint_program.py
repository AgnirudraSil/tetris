import pygame
import tools

screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Make You own Textures!")
screen.fill((40, 40, 40))
gap = 640 // 40
canvas_holder = [[[255, 255, 255] for i in range(40)] for j in range(40)]
pencil = tools.Pencil()
marquee = tools.Marquee()
eraser = tools.Eraser()
hand = tools.Hand()
reset = tools.Reset()
eyedropper = tools.Eyedropper()
gradient = tools.Gradient()
zoom = tools.Zoom()
toolbar = pygame.Surface((32, 720))
swatch = pygame.Surface((600, 720))
canvas = pygame.Surface((640, 640))
canvas_pos = [72, 40]
rect = [0, 0, 0, 0]
color = (0, 0, 0)


def draw_grid():
    for i in range(40):
        for j in range(40):
            pygame.draw.rect(canvas, canvas_holder[i][j], (i * (640 // 40), j * (640 // 40), 640 // 40, 640 // 40))
    for i in range(40):
        pygame.draw.line(canvas, (181, 181, 181), (i * gap, 0), (i * gap, 640))
        pygame.draw.line(canvas, (181, 181, 181), (0, i * gap), (640, i * gap))


def reset_display():
    screen.fill((40, 40, 40))
    toolbar.fill((83, 83, 83))
    swatch.fill((83, 83, 83))
    canvas.fill((255, 255, 255))
    draw_grid()
    pygame.draw.rect(canvas, (43, 43, 43), rect, 2)
    pencil.draw(toolbar)
    eraser.draw(toolbar)
    reset.draw(toolbar)
    marquee.draw(toolbar)
    zoom.draw(toolbar)
    gradient.draw(toolbar)
    hand.draw(toolbar)
    eyedropper.draw(toolbar)
    screen.blit(canvas, canvas_pos)
    screen.blit(toolbar, (0, 0))
    screen.blit(swatch, (760, 0))


running = True

while running:
    count = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if marquee.select is True:
                    marquee.set_initial(event.pos)
                if hand.select is True:
                    hand.set_initial(event.pos)
        if pygame.mouse.get_pressed()[0]:
            pencil.selected(event.pos, eraser, hand, zoom, gradient, marquee, eyedropper)
            canvas_holder = pencil.function(event.pos, canvas_holder, color)
            canvas_holder = eraser.function(event.pos, canvas_holder)
            eraser.selected(event.pos, pencil, hand, zoom, gradient, marquee, eyedropper)
            marquee.selected(event.pos, eraser, pencil, hand, zoom, gradient, eyedropper)
            if marquee.select is True:
                rect = marquee.function(event.pos)
            if hand.select is True:
                canvas_pos = hand.function(event.pos)
            if reset.select is not None:
                canvas_pos = reset.selected(event.pos, canvas_pos, pencil,
                                            eraser, hand, zoom, gradient, marquee, eyedropper)
            hand.selected(event.pos, eraser, pencil, zoom, gradient, eyedropper, marquee)
            eyedropper.selected(event.pos, eraser, pencil, zoom, gradient, hand, marquee)
            gradient.selected(event.pos, eraser, pencil, zoom, eyedropper, hand, marquee)
            zoom.selected(event.pos, eraser, pencil, gradient, eyedropper, hand, marquee)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LCTRL and eyedropper.select is True:
                if count == 0:
                    count += 1
                    color = eyedropper.function()
                    eyedropper.select = False
                    pencil.select = True
                    pencil.select_()
            eyedropper.unselect()
        if pygame.key.get_pressed()[pygame.K_LCTRL] and pygame.key.get_pressed()[pygame.K_d]:
            marquee.initial = [0, 0]
            marquee.diff = [0, 0]
            rect = [0, 0, 0, 0]
    reset_display()
    pygame.display.flip()

pygame.quit()