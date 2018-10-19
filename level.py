
from entity import Entity, Agent, Projectile, Star

import pygame

class Camera:
    """ This class is used to get different views into the level. This will
        handle correctly transforming and scaling the Entity's in the level,
        prepping them to get rendered propperly.
    """
    def __init__(self):
        self.loc = [0.0, 0.0]
        self.zoom = 1.0
        self.move_speed = 1.0

    def move_to(self, loc):
        self.loc = loc

    def zoom_in(self, z):
        """ Increments the camera's zoom level by the given amount. The zoom
            value will never go below 0.1 or above 2.0.
        """
        self.zoom += z
        if self.zoom <= 0.1:
            self.zoom = 0.1
        if self.zoom >= 2.0:
            self.zoom = 2.0

    def get_zoom(self):
        """ Returns the zoom value of the object. """
        return self.zoom

    def get_screen_space(self, window, loc):
        """ Convert game-space of an Entity location into screen-space to be
            displayed in an image.
        """
        # Get the differences in location
        dif_loc = [self.loc[0] - loc[0], self.loc[1] - loc[1]]
        # Scale those differences
        dif_loc[0] *= self.zoom
        dif_loc[1] *= self.zoom
        # Adjust for screen size
        dif_loc[0] += window.get_width()/2
        dif_loc[1] += window.get_height()/2
        return dif_loc

    def pointer_game_space(self, window, loc):
        """ Convert pixel location on screen into game-space. """
        """
        # Given the pixel coordinates
        dif_loc = [self.loc[0], self.loc[1]]
        # Adjust for screen size
        dif_loc[0] -= window.get_width()/2
        dif_loc[1] -= window.get_height()/2
        # Scale
        dif_loc[0] /= self.get_zoom()
        dif_loc[1] /= self.get_zoom()
        # Translate
        dif_loc[0] += loc[0]
        dif_loc[1] += loc[1]
        return dif_loc
        """
        return [
                -window.get_width()/2  / self.zoom + loc[0] - self.loc[0],
                -window.get_height()/2 / self.zoom + loc[1] - self.loc[1],
               ]

class Level:
    def __init__(self, player, ents, agents, stars):
        # View into the level
        self.cam = Camera()
        # Set of Entity sets that the level will manage
        self.player = player
        self.entity_list = ents
        self.star_list = stars
        self.agent_list = agents
        self.projectile_list = []
        # self.background = ""

    def add_ent(self, ent):
        """ Adds the given Entity to one of the Level's internal lists of
            Entitys.
        """
        if   type(ent) == Star:
            self.star_list.append(ent)
        elif type(ent) == Projectile:
            self.projectile_list.append(ent)
        elif type(ent) == Agent:
            self.agent_list.append(ent)
        elif type(ent) == Entity:
            self.entity_list.append(ent)
        else:
            print("Err: Couldn't add object to level!")

    def step_physics(self, dt):
        """ Iterate the physics for all of the Entity's in then level. This
            is a simple leap frog iterator. Pretty much to calculate the new
            location for each object, we need find the integral of it, and
            then the integral of that. This essentially boils down to finding
            the force applied to each object, increment the velocity by that,
            then increment the location by that.
        """
        self.player.iterate_force(self.star_list)
        for e in self.entity_list:
            e.iterate_force(self.star_list)
        self.player.iterate_velocity(dt)
        for e in self.entity_list:
            e.iterate_velocity(dt)
        for e in self.entity_list:
            e.iterate_location(dt)
            # Reset the forces applied, so that we don't super charge the
            # velocities for all of the entities
            e.clear_force()
        self.player.iterate_location(dt)
        self.player.clear_force()

    def draw_all(self, window):
        # Clear the window so that all of the pixels are black
        window.fill([0,0,0])
        # Step through each list, and draw the Entitys
        for e in self.star_list:
            e.draw(window, self.cam)
        for e in self.agent_list:
            e.draw(window, self.cam)
        for e in self.entity_list:
            e.draw(window, self.cam)
        for e in self.projectile_list:
            e.draw(window, self.cam)
        # Don't forget to draw the player!
        self.player.draw(window, self.cam)
        # The currently drawn image was the back-buffer.
        # So now we need to swap buffers so the image displays.
        pygame.display.flip()


