
from entity import Entity, Enemy, Player, Projectile, Star

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


