#!/usr/bin/env python3

class Button:
	""" A clickable object """
	def __init__(self, image, rect, action):
		"""
			Initialize a button

			Arguments:
			image -- Image representing the button on-screen
			rect -- The x and y coordinates and the height and width of the button
			action -- action upon click of the button as a lambda function
		"""
		self.image = image
		self.rect = rect
		self.action = action
	
	def contains(self, point):
		""" Checks if the point is within the button's bounds """
		return point[0] >= self.rect[0] and point[0] <= self.rect[0] + self.rect[2] and \
				point[1] >= self.rect[1] and point[1] <= self.rect[1] + self.rect[3]

	def click(self):
		""" Invokes the button's action. """
		self.action()
