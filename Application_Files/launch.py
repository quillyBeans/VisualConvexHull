import pygame
from pygame.locals import *
from convexHull import convexHull


class Button:
    def __init__(self, button_message, coordinates):
        self.caption = " "+button_message
        self.btn_width = 90
        self.btn_height = 30
        self.rect = pygame.Rect(coordinates[0], coordinates[1], self.btn_width, self.btn_height)
        self.surface = pygame.Surface(self.rect.size)
        self.bg_color = pygame.Color(b'lightgray')
        self.fg_color = pygame.Color(b'black')
        pygame.font.init()
        self.font = pygame.font.Font('freesansbold.ttf', 14)
        self._update()

    def pressed(self, mouse):
        # if mouse right or left is within the button
        if mouse[0] > self.rect.topleft[0] and mouse[1] > self.rect.topleft[1]:
            if mouse[0] < self.rect.bottomright[0] and mouse[1] < self.rect.bottomright[1]:
                return True
        return False

    def draw(self, display_surface):
        display_surface.blit(self.surface, self.rect)

    def _update(self):
        w = self.rect.width
        h = self.rect.height

        # fill the button background
        self.surface.fill(self.bg_color)
        # render the caption and return a rectangle
        caption_surf = self.font.render(self.caption, True, self.fg_color, self.bg_color)
        caption_rect = caption_surf.get_rect()
        # inflate in place, moves the text to a more pleasing spot in the button
        caption_rect.inflate_ip(-10, -17)
        # commits the caption
        self.surface.blit(caption_surf, caption_rect)

        # draw border for normal button
        pygame.draw.rect(self.surface, pygame.Color(b'black'), pygame.Rect((0, 0, w, h)), 1)
        pygame.draw.line(self.surface, pygame.Color(b'white'), (1, 1), (w - 2, 1))
        pygame.draw.line(self.surface, pygame.Color(b'white'), (1, 1), (1, h - 2))
        pygame.draw.line(self.surface, pygame.Color(b'darkgray'), (1, h - 1), (w - 1, h - 1))
        pygame.draw.line(self.surface, pygame.Color(b'darkgray'), (w - 1, 1), (w - 1, h - 1))
        pygame.draw.line(self.surface, pygame.Color(b'gray'), (2, h - 2), (w - 2, h - 2))
        pygame.draw.line(self.surface, pygame.Color(b'gray'), (w - 2, 2), (w - 2, h - 2))


class App:
    def __init__(self):
        self.button_width = 20
        self.button_spacing = 100
        self.button_offset = 0
        self.button_right_most = 840
        self.msg_display_top_left = 20, 25
        self.running = True
        self.display_surf = None
        self.size = self.weight, self.height = 960, 720
        self.bg_color = None
        self.point_color = None
        self.hull_color = None
        self.mouse_x, self.mouse_y = 0, 0
        self.font_obj = None
        self.points = []
        self.ch_points = []
        self.msg = "Click points then 'Get Hull'"
        # self.btn_interactive = Button("Interactive", (self.button_right_most - self.button_offset, self.button_width))
        # self.button_offset = self.button_spacing
        self.btn_reset = Button("Reset", (self.button_right_most - self.button_offset, self.button_width))
        self.button_offset += self.button_spacing
        self.btn_get_convex = Button("Get Hull", (self.button_right_most - self.button_offset, self.button_width))

    def on_init(self):
        pygame.init()
        self.font_obj = pygame.font.Font('freesansbold.ttf', 24)
        self.bg_color = pygame.Color(0, 0, 0)
        self.point_color = pygame.Color(255, 255, 255)
        self.hull_color = pygame.Color(b'red')
        self.display_surf = pygame.display.set_mode(self.size)
        self.running = True

    def on_event(self, event):
        if event.type == QUIT:
            self.running = False
        elif event.type == MOUSEBUTTONUP and event.button in (1, 2, 3):
            # if event is button, make hull or reset screen, else add to point list
            if self.btn_get_convex.pressed(event.pos):
                self.msg = "Convex Hull"
                del self.ch_points[:]
                self.ch_points = convexHull(self.points)
            elif self.btn_reset.pressed(event.pos):
                del self.points[:]
                del self.ch_points[:]
                self.msg = "Click points then 'Get Hull'"
            else:
                self.points.append(event.pos)
                self.msg = "x , y :  " + str(event.pos)

    def on_loop(self):
        self.display_surf.fill(self.bg_color)
        self.btn_get_convex.draw(self.display_surf)
        self.btn_reset.draw(self.display_surf)
        # self.btn_interactive.draw(self.display_surf)

        # draws out the regular coordinate dots if populated
        for coord in self.points:
            pygame.draw.circle(self.display_surf, self.point_color, coord, 3, 0)
        # draws out the convex hull coordinate dots if populated
        for coord in self.ch_points:
            pygame.draw.circle(self.display_surf, self.hull_color, coord, 3, 0)
        # draws the edges to show the convex hull if populated
        if len(self.ch_points) > 0:
            pygame.draw.lines(self.display_surf, self.hull_color, True, self.ch_points, 1)

        # message display window
        msg_surface_obj = self.font_obj.render(self.msg, False, self.point_color)
        msg_rect_obj = msg_surface_obj.get_rect()
        msg_rect_obj.topleft = (self.msg_display_top_left[0], self.msg_display_top_left[1])
        self.display_surf.blit(msg_surface_obj, msg_rect_obj)

    def on_render(self):
        pygame.display.update()

    def on_cleanup(self):
        pygame.quit()

    def execute(self):
        self.on_init()
        while self.running:
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()

if __name__ == "__main__":
    lets_go = App()
    lets_go.execute()

