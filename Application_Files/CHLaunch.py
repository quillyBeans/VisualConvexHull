import pygame
from pygame.locals import *
from convexHull import convexHull

class Button:
	def __init__(self, buttonMessage, coordinates):
		self.caption = " "+buttonMessage
		self.rect = pygame.Rect(coordinates[0], coordinates[1], 80, 25)
		self.surface = pygame.Surface(self.rect.size)
		self.bgcolor = pygame.Color(b'lightgray')
		self.fgcolor = pygame.Color(b'black')
		pygame.font.init()
		self.font = pygame.font.Font('freesansbold.ttf', 14)
		self._update()

	def pressed(self,mouse):
		if mouse[0] > self.rect.topleft[0] and mouse[1] > self.rect.topleft[1]:
			if mouse[0] < self.rect.bottomright[0] and mouse[1] < self.rect.bottomright[1]:
				return True
		return False
		'''
					else: return False
				else: return False
			else: return False
		else: return False
		'''
		
	def draw(self, displaySurface):
		displaySurface.blit(self.surface, self.rect)
			
	def _update(self):
		w = self.rect.width
		h = self.rect.height
		
		self.surface.fill(self.bgcolor)
		captionSurf = self.font.render(self.caption, True, self.fgcolor, self.bgcolor)
		captionRect = captionSurf.get_rect()
		self.surface.blit(captionSurf, captionRect)
		
		# draw border for normal button
		pygame.draw.rect(self.surface, pygame.Color(b'black'), pygame.Rect((0, 0, w, h)), 1) # black border around everything
		pygame.draw.line(self.surface, pygame.Color(b'white'), (1, 1), (w - 2, 1))
		pygame.draw.line(self.surface, pygame.Color(b'white'), (1, 1), (1, h - 2))
		pygame.draw.line(self.surface, pygame.Color(b'darkgray'), (1, h - 1), (w - 1, h - 1))
		pygame.draw.line(self.surface, pygame.Color(b'darkgray'), (w - 1, 1), (w - 1, h - 1))
		pygame.draw.line(self.surface, pygame.Color(b'gray'), (2, h - 2), (w - 2, h - 2))
		pygame.draw.line(self.surface, pygame.Color(b'gray'), (w - 2, 2), (w - 2, h - 2))
		
		
class App:
	def __init__(self):
		self.running = True
		self.display_surf = None
		self.size = self.weight, self.height = 640, 480
		self.bg_color = None
		self.point_color = None
		self.hull_color = None
		self.mousex, self.mousey = 0, 0
		self.fontObj = None
		self.points = []
		self.chPoints = []
		self.msg = 'debug area'
		#self.soundClick = pygame.mixer.Sound("?")
		self.getConvexBtn = Button("Get Hull", (400, 20))
		self.resetBtn = Button("Reset", (500, 20))
		
	def on_init(self):
		pygame.init()
		self.fontObj = pygame.font.Font('freesansbold.ttf', 24)
		self.bg_color = pygame.Color(0,0,0)
		self.point_color = pygame.Color(255,255,255)
		#self.hull_color = pygame.Color(0,255,0)
		self.hull_color = pygame.Color(b'red')
		self.display_surf = pygame.display.set_mode(self.size)
		self.running = True

	def on_event(self, event):
		if event.type == QUIT:
			self.running = False
		elif event.type == MOUSEBUTTONUP and event.button in (1, 2, 3):
			if self.getConvexBtn.pressed(event.pos):
				self.msg = "convex hull"
				del self.chPoints[:]
				self.chPoints = convexHull(self.points)
			elif self.resetBtn.pressed(event.pos):
				del self.points[:]
				del self.chPoints[:]
				self.msg = "reset"
			else:
				# soundObj.play()
				self.points.append(event.pos)
				self.msg = str(event.pos)
	
	def on_loop(self):
		self.display_surf.fill(self.bg_color)
		self.getConvexBtn.draw(self.display_surf)
		self.resetBtn.draw(self.display_surf)

		for coord in self.points:
			pygame.draw.circle(self.display_surf, self.point_color, coord, 3, 0)
		for coord in self.chPoints:
			pygame.draw.circle(self.display_surf, self.hull_color, coord, 3, 0)

		# debugging
		msgSurfaceObj = self.fontObj.render(self.msg, False, self.point_color)
		msgRectobj = msgSurfaceObj.get_rect()
		msgRectobj.topleft = (10, 20)
		self.display_surf.blit(msgSurfaceObj, msgRectobj)
	
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
	letsGo = App()
	letsGo.execute()

