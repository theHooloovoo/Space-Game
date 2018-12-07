#!/usr/bin/env python3
""" File for GUI Objects

	Currently only contains Button class that represents a selectable
	button on screen.
"""

BTN_HIGHLIGHT = 255
BTN_NORMAL = 190

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
        self.image = image.convert()
        self.image.set_alpha(BTN_NORMAL)
        self.rect = rect
        self.action = action

    def highlight(self, b):
        """ Highlights the button by increasing the alpha """
        if b:
            self.image.set_alpha(BTN_HIGHLIGHT)
        else:
            self.image.set_alpha(BTN_NORMAL)

    def contains(self, point):
        """ Checks if the point is within the button's bounds """
        return point[0] >= self.rect[0] and point[0] <= self.rect[0] + self.rect[2] and \
                point[1] >= self.rect[1] and point[1] <= self.rect[1] + self.rect[3]

    def click(self):
        """ Invokes the button's action. """
        self.action()

    def draw(self, window):
        """ Draws the button to the the surface """
        window.blit(self.image, self.rect[:2])

class TextButton:
    """ A clickable object """
    def __init__(self, font, text, pos, action):
        """
            Initialize a button

            Arguments:
            font -- Font to render text with
            text -- Text to render
            pos -- X and Y coordinate of the button
            action -- action upon click of the button as a lambda function
        """
        self.image = font.render(text, False, [255, 255, 255])
        self.image.set_alpha(BTN_NORMAL)
        self.pos = pos
        self.action = action

    def highlight(self, b):
        """ Highlights the button by increasing the alpha """
        if b:
            self.image.set_alpha(BTN_HIGHLIGHT)
        else:
            self.image.set_alpha(BTN_NORMAL)

    def click(self):
        """ Invokes the button's action. """
        self.action()

    def draw(self, window):
        """ Draws the button to the the surface """
        window.blit(self.image, self.pos)
