import pygame 
import pygame.camera
from pygame.locals import *

pygame.init()
pygame.camera.init()
size = (640, 480)

shrunken = (320, 240)
b = (0, 0, 0xFF)
r = (0xFF, 0, 0)
t = (0x5A, 0xAA, 0xAA)
d = pygame.display.set_mode(size, 0)
s = pygame.surface.Surface(size, 0, d)
c = pygame.camera.list_cameras()
cam = pygame.camera.Camera(c[0], size, "HSV")
cam.start()

going = True 

last_array = None
diffs = None
s = pygame.surface.Surface(size)

while going:
	if cam.query_image():
		s = cam.get_image(s)
		s2d = pygame.surfarray.array2d(s)
		s2d = numpy.bitwise_and(s2d, 0xFF)
		diffs = s2d
		if last_array is not None:
			diffs = s3d - last_array
			print last_array

		last_array = s2d
		pygame.surfarray.blit_array(s, diffs)
		
		p = pygame.transform.scale(s, size)
		d.blit(p, (0, 0))
		m = pygame.mask.from_threshold(s, b, t)
		for blob in m.connected_components(10):
			coord = blob.centroid()
			pygame.draw.circle(s, r, coord, 50, 5)

		pygame.display.flip()
		for e in pygame.event.get():
			if e.type == QUIT:
				cam.stop()
				going = False
