""" entity.py Test Suite
"""

from math import sqrt
import unittest
import entity

class Ent:
    """ Dummy class for testing """
    def __init__(self):
        self.loc = [0, 0]
        self.vel = [0.0, 0.0]
        self.rotation = 0
        self.radius = 0
        self.image_proj = 0

class EntityTest(unittest.TestCase):
    def __init__(self):
        pass

    def run_tests(self):
        """ """
        print("Running Entity Test Suite")
        self.test_entity()
        self.test_agent()
        self.test_projectile()
        print("Entity Test Suite Complete")

    def test_entity(self):
        """ """
        print("|\tRunning Entity Tests...")
        self.test_entity_distance_to()
        self.test_entity_is_touching()

    def test_entity_distance_to(self):
        """ """
        print("|\t|\tTesting Entity.distance_to()...")
        e1 = entity.Entity([0, 0], [0, 0], 10, 50, 0, 0)
        e2 = entity.Entity([100, 100], [0, 0], 10, 150, 0, 0)
        e3 = entity.Entity([320, 500], [0, 0], 10, 10, 0, 0)

        self.assertTrue(e1.distance_to(e1) == 0, "Test 1.1 Failed")
        self.assertTrue(e1.distance_to(e2) == sqrt(20000), "Test 1.2 Failed")
        self.assertTrue(e1.distance_to(e3) == sqrt(352400), "Test 1.3 Failed")
        self.assertTrue(e3.distance_to(e2) == sqrt(208400), "Test 1.4 Failed")

    def test_entity_is_touching(self):
        """ """
        print("|\t|\tTesting Entity.is_touching()...")
        e1 = entity.Entity([0, 0], [0, 0], 10, 50, 0, 0)
        e2 = entity.Entity([100, 100], [0, 0], 10, 150, 0, 0)
        e3 = entity.Entity([320, 500], [0, 0], 10, 10, 0, 0)

        self.assertTrue(e1.is_touching(e2), "Test 2.1 Failed")
        self.assertFalse(e1.is_touching(e3), "Test 2.2 Failed")
        self.assertFalse(e2.is_touching(e3), "Test 2.3 Failed")

    def test_agent(self):
        """ """
        print("|\tRunning Agent Tests...")

    def test_projectile(self):
        """ """
        print("|\tRunning Projectile Tests...")
        self.test_projectile_iterate_location()

    def test_projectile_iterate_location(self):
        """ """
        print("|\t|\tTesting Projectile.iterate_location()...")
        p1 = entity.Projectile(Ent(), 10, 0, 10)
        p1.loc = [0, 0]
        p1.vel = [10, 10]
        p1.iterate_location(1)
        self.assertTrue(p1.loc == [10, 10], "Tests 1.1 Failed")
        p1.vel = [-10, -10]
        p1.iterate_location(1)
        self.assertTrue(p1.loc == [0, 0], "Tests 1.2 Failed")
