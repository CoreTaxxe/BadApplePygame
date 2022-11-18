import pygame
import numpy
from videoplayer import VideoPlayer

pygame.init()

# use rectangles instead of images
pixel = False

# render resolution (for pixelation)
resolution = [100, 100]

# actual screen
screen = pygame.display.set_mode([1200, 1200])

# black to white conversion threshold 
thresh_hold = [255 / 2, 255 / 2, 255 / 2]

# create videoplayer reference
# custom class -> poorly optimized
ref_video = VideoPlayer("bad_apple.mp4", resolution=resolution, position=(900, 900))


org = pygame.image.load("white_pg_logo.png").convert()
img = pygame.transform.scale(org, [screen.get_size()[0] // resolution[0], screen.get_size()[1] // resolution[1]])

print(img.get_size())

# invert colors
def inverted(_img):
    inv = pygame.Surface(_img.get_rect().size, pygame.SRCALPHA)
    inv.fill((255, 255, 255, 255))
    inv.blit(_img, (0, 0), None, pygame.BLEND_RGB_SUB)
    return inv


img.set_colorkey((0, 0, 0))

white_scale = img
black_scale = inverted(img)

black_scale.set_colorkey((255, 255, 255))

if pixel:
    black_scale = pygame.Surface([screen.get_size()[0] // resolution[0], screen.get_size()[1] // resolution[1]])
    black_scale.fill((0, 0, 0))

    white_scale = pygame.Surface([screen.get_size()[0] // resolution[0], screen.get_size()[1] // resolution[1]])
    white_scale.fill((255, 255, 255))

clock = pygame.time.Clock()

# pos
ref_video.set_screen_position(
    (
        screen.get_size()[0] - ref_video.get_surface().get_size()[0],
        screen.get_size()[1] - ref_video.get_surface().get_size()[1]
    )
)

ref_video.play()
scale = 1
hide = False
while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_SPACE:
                if ref_video.isplaying:
                    ref_video.pause()
                else:
                    ref_video.unpause()

            if event.key == pygame.K_h:
                hide = not hide

            # does not work properly
            if event.key == pygame.K_w:
                scale += 0.1
                img = pygame.transform.scale(org,
                                             [
                                                 int((screen.get_size()[0] // resolution[0])*scale),
                                                 int((screen.get_size()[1] // resolution[1])*scale)
                                             ]
                                             )

                img.set_colorkey((0, 0, 0))
                print(img.get_size())

                white_scale = img
                black_scale = inverted(img)

                black_scale.set_colorkey((255, 255, 255))

            # does not work properly
            if event.key == pygame.K_s:
                scale -= 0.1
                img = pygame.transform.scale(org,
                                             [
                                                 int((screen.get_size()[0] // resolution[0])*scale),
                                                 int((screen.get_size()[1] // resolution[1])*scale)
                                             ]
                                             )
                print(img.get_size())
                img.set_colorkey((0, 0, 0))

                white_scale = img
                black_scale = inverted(img)

                black_scale.set_colorkey((255, 255, 255))


    screen.fill([0, 0, 0])

    ref_video.update()

    # get current frame as pygame surface
    frame = ref_video.get_surface()

    # loop through pixels
    for y in range(int(resolution[1] / scale)):
        for x in range(int(resolution[0] / scale)):
            r, g, b, a = frame.get_at((int(x), int(y)))

            if r < thresh_hold[0] and g < thresh_hold[1] and b < thresh_hold[2]:
                screen.blit(black_scale,
                            (int((x * black_scale.get_size()[0])), int((y * black_scale.get_size()[1]))))
            else:
                screen.blit(white_scale, (int((x * black_scale.get_size()[0])), int((y * black_scale.get_size()[1]))))

    # player.update()
    # player.render(screen)
    pygame.display.set_caption(str(clock.get_fps()))

    if not hide:
        ref_video.render(screen)
    pygame.display.flip()
    clock.tick()
