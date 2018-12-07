""" Runs all the test suites """

from level_tests import LevelTest
from entity_tests import EntityTest

et = EntityTest()
lt = LevelTest()

print("---Test Suite for Space-Game-----------------")
print("Tests the entity and level modules.")
print("Does not test the states or gui modules.")
print("---------------------------------------------\n")

et.run_tests()
lt.run_tests()
