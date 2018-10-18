
from entity import Entity, Enemy, Player, Projectile, Star

class Camera:
    def __init__(self, width, height):
        self.loc = [0.0, 0.0]
        self.width = width
        self.height = height
        self.zoom = 1.0

    def move_to(self, loc):
        self.loc = loc

    def zoom_in(self, z):
        """ Increments the cameras zoom level by the given amount. The zoom
            value will never go below 0.1 or above 2.0.
        """
        self.zoom += z
        if self.zoom <= 0.1:
            self.zoom = 0.1
        if self.zoom >= 2.0:
            self.zoom = 2.0

    def get_zoom(self):
        return self.zoom

class Level:
    def __init__(self):
        self.entity_list = []
        self.star_list = []
        # self.background = ""

    def step_physics(self, dt):
        for e in self.entity_list:
            e.iterate_force(self.star_list)

        for e in self.entity_list:
            e.iterate_velocity(dt)

        for e in self.entity_list:
            e.iterate_location(dt)
            e.clear_force()
            # e.look_at(self.star_list[0])


