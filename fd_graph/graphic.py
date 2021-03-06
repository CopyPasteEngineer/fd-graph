import pygame

from . import config


class GraphicObject:
    def update(self):
        raise NotImplementedError()

    def draw(self, screen):
        raise NotImplementedError()


class GraphicScreen:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.screen = None
        self.running = False

        self.background_color = config.get('game.color')
        self.fps = 30

        self.objects = []

    def start(self):
        pygame.init()

        self.screen = pygame.display.set_mode((self.width, self.height))
        self.running = True

        clock = pygame.time.Clock()
        play = not config.get('game.prompt')
        first = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        play = not play

            if play or first:
                self.screen.fill(self.background_color)

                for o in self.objects:
                    o.update()

                for o in self.objects:
                    o.draw(self.screen)

                first = False
            pygame.display.flip()
            clock.tick(self.fps)

        pygame.quit()

    def add_object(self, obj: GraphicObject):
        self.objects.append(obj)
