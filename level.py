#!usr/bin/env python3
""" Level and view classes

	Classes used as, somewhat, of a model component of MVC.
	The Camera helps view the player and the Level contains
	all the data used by the GameState to generate the level.
"""

import math
from math import sqrt

import copy
from copy import copy

import pygame

from entity import Entity, Agent, Projectile, Star

class Camera:
    """ This class is used to get different views into the level. This will
        handle correctly transforming and scaling the Entity's in the level,
        prepping them to get rendered propperly.
    """
    def __init__(self):
        self.loc = [0.0, 0.0]
        self.zoom = 1.0
        self.move_speed = 1.0

    def __copy__(self):
        """ Copies the camera object. """
        cls = self.__class__
        result = cls.__new__(cls)
        result.__dict__.update(self.__dict__)
        result.loc = self.loc.copy()
        return result

    def move_to(self, loc):
        """ Moves camera to a new location """
        self.loc = loc

    def zoom_in(self, zoom):
        """ Increments the camera's zoom level by the given amount. The zoom
            value will never go below 0.1 or above 2.0.
        """
        self.zoom += zoom
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
        # Given the pixel coordinates
        dif_loc = [-1 * (loc[0] - window.get_width() / 2),
                   -1 * (loc[1] - window.get_height() / 2)]
        # Scale
        dif_loc[0] /= self.get_zoom()
        dif_loc[1] /= self.get_zoom()
        # Translate
        dif_loc[0] += self.loc[0]
        dif_loc[1] += self.loc[1]
        return dif_loc

class Level:
    """ Contains all data related to the level
    """
    def __init__(self, player, ents, agents, stars):
        """ Initializes the level with entities

			Arguments:
			player -- The player class
			ents -- List of entities in the level
			agents -- List of agents in the level
			stars -- List of stars in the level
        """
        # View into the level
        self.cam = Camera()
        # Set of Entity sets that the level will manage
        self.player = player
        self.entity_list = ents
        self.star_list = stars
        self.agent_list = agents
        self.projectile_list = []
        # self.background = ""

    def __copy__(self):
        """ """
        cls = self.__class__
        result = cls.__new__(cls)
        result.__dict__.update(self.__dict__)
        # Copy each object in the lists over
        e_vec = []
        a_vec = []
        s_vec = []
        for e in self.entity_list:
            e_vec.append(copy(e))
        for a in self.agent_list:
            a_vec.append(copy(a))
        for s in self.star_list:
            s_vec.append(copy(s))
        result.entity_list = e_vec
        result.agent_list = a_vec
        result.star_list = s_vec
        result.projectile_list = []
        result.player = copy(self.player)
        return result

    def collision_check(self, dt):
        """ Checks entities for collision

			Attributes:
			dt -- The time that has passed since last iteration
        """
        # Check against Stars
        for sun in self.star_list:
            for ent in self.entity_list:
                if sun.is_touching(ent):
                    ent.is_active = False
                    # print("Touched the sun!")
            for proj in self.projectile_list:
                if sun.is_touching(proj):
                    proj.is_active = False
                    # print("Touched the sun!")
            for agent in self.agent_list:
                if sun.is_touching(agent):
                    agent.is_active = False
                    # print("Touched the sun!")
            if sun.is_touching(self.player):
                self.player.is_active = False
                # print("Collision with Player detected.")
        # Check Entities
        for ent in self.entity_list:
            for ent2 in self.entity_list:
                if ent != ent2 and ent.is_touching(ent2):
                    ent.resolve_collisions(ent2)
            for agent in self.agent_list:
                if ent.is_touching(agent):
                    ent.resolve_collisions(agent)
            for proj in self.projectile_list:
                if ent.is_touching(proj):
                    ent.resolve_collisions(proj)
        # Check Agents
        for ent in self.agent_list:
            for agent in self.agent_list:
                if ent != agent and ent.is_touching(agent):
                    ent.resolve_collisions(agent)
                    ent.harm(0.1 * dt)
            for proj in self.projectile_list:
                if ent != proj and ent.is_touching(proj):
                    ent.resolve_collisions(proj)
                    ent.harm(proj.damage)
                    proj.is_active = False
        # Check Projectiles
        for ent in self.projectile_list:
            for proj in self.projectile_list:
                if ent != proj and ent.is_touching(proj):
                    ent.resolve_collisions(proj)
                    ent.is_active = False
        # Check Player
        for ent in self.entity_list:
            if self.player.is_touching(ent):
                self.player.resolve_collisions(ent)
                self.player.harm(0.1 * dt)
        for agent in self.agent_list:
            if self.player.is_touching(agent):
                self.player.resolve_collisions(agent)
                self.player.harm(0.1 * dt)
                agent.harm(0.1 * dt)
        for proj in self.projectile_list:
            if self.player.is_touching(proj):
                # self.player.resolve_collisions(proj)
                self.player.harm(proj.damage)
                proj.is_active = False

    def cull_ents(self, dt):
        """ This does something """
        # Remove an entity if they are not active.
        # Easy way of destructively mutating a list
        self.entity_list = [n for n in self.entity_list
                            if n.is_active]
        self.agent_list = [n for n in self.agent_list
                           if n.is_active]
        self.projectile_list = [n for n in self.projectile_list
                                if n.is_active]
        # Tick each of the projectile durations
        for proj in self.projectile_list:
            proj.duration -= 0.01 * dt
        self.projectile_list = [n for n in self.projectile_list
                                if n.duration > 0.0]

    def add_ent(self, ent):
        """ Adds the given Entity to one of the Level's internal lists of
            Entitys.
        """
		# pylint: disable=C0123
        if   type(ent) == Star:
            self.star_list.append(ent)
        elif type(ent) == Projectile:
            self.projectile_list.append(ent)
        elif type(ent) == Agent:
            self.agent_list.append(ent)
        elif type(ent) == Entity:
            self.entity_list.append(ent)
        else:
            print("Err: Couldn't add object to level!", type(ent))
        # pylint: enable=C0123

    def step_game_logic(self, dt):
        """ Iterates the game information and mechanics

			Arguments:
			dt -- Time passed since last iteration
        """
        self.collision_check(dt)
        self.cull_ents(dt)
        # This part is for testing!
        for ent in self.agent_list:
            ent.look_at(self.player)
            ent.use_booster(dt)
        # Player logic
        if self.player.health <= 0.0:
            self.add_ent(self.player.explode())
        self.player.use_booster(dt)
        self.player.turn(dt)
        self.player.booster_fuel += 0.03 * dt
        if self.player.booster_fuel > self.player.booster_fuel_max:
            self.player.booster_fuel = self.player.booster_fuel_max
        # Enemy Logic
        for agent in self.agent_list:
            if agent.health <= 0.0 and agent.is_active:
                for n in agent.explode():
                    self.add_ent(n)
                # Make sure the agent doesn't re-explode!
                agent.is_active = False
                # print("exploded")
        for n in range(0, len(self.agent_list), -1):
            if self.agent_list[n].is_alive:
                self.agent_list.remove(self.agent_list[n])
        # Move camera
        d_sqrd = self.player.loc[0] ** 2 + self.player.loc[1] ** 2
        mod = 1 - (1 / (1 + (0.00001 * d_sqrd))) # Fancy math
        self.cam.loc = [self.player.loc[0] * mod, self.player.loc[1] * mod]

    def step_physics(self, dt):
        """ Iterate the physics for all of the Entity's in the level. This
            is a simple leap frog iterator. Pretty much, to calculate the new
            location for each object, we need find the net force applied on
            the object by all of the stars, then add that to the velocity
            (accounting for the time step 'dt'). Then update the location by
            the velocity (again, accounting for 'dt').
        """
        # Force
        self.player.iterate_force(self.star_list)
        for e in self.entity_list:
            e.iterate_force(self.star_list)
        for e in self.agent_list:
            e.iterate_force(self.star_list)
        for e in self.projectile_list:
            e.iterate_force(self.star_list)
        # Velocity
        self.player.iterate_velocity(dt)
        for e in self.entity_list:
            e.iterate_velocity(dt)
        for e in self.agent_list:
            e.iterate_velocity(dt)
        for e in self.projectile_list:
            e.iterate_velocity(dt)
        # Location
        self.player.iterate_location(dt)
        for e in self.entity_list:
            e.iterate_location(dt)
        for e in self.agent_list:
            e.iterate_location(dt)
        for e in self.projectile_list:
            e.iterate_location(dt)
        # Reset the forces applied, so that we don't super charge the
        # velocities for all of the entities
        self.player.clear_force()
        for e in self.entity_list:
            e.clear_force()
        for e in self.agent_list:
            e.clear_force()
        for e in self.projectile_list:
            e.clear_force()

    def cull_far(self):
        for a in self.agent_list:
            if sqrt(a.loc[0]**2 + a.loc[1]**2) >= 1000:
                a.is_active = False

    def draw_all(self, window):
        """ Draws all the entities in the level

			Arguments:
			window -- Surface to draw entities to
        """
        # Clear the window so that all of the pixels are black
        window.fill([0, 0, 0])
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
