""" level.py Test Suite
"""
import unittest
import level

class Window():
    """ Test class imitating the main window of the game """
    def get_width(self):
        return 1280
    def get_height(self):
        return 800

class LevelTest(unittest.TestCase):
    def __init__(self):
        self.cam = level.Camera()
        self.window = Window()

    def run_tests(self):
        """ Runs all the tests associated with this class """
        print("Running Level Test Suite")
        self.test_camera()
        print("Level Test Suite Complete")

    def test_camera(self):
        """ Wrapper method for all camera class related tests"""
        print("|\tRunning Camera Tests...")
        # self.test_camera_get_screen_space()
        self.test_camera_pointer_game_space()

    def test_camera_pointer_game_space(self):
        print("|\t|\tTesting Camera.pointer_game_space()...")
        loc1 = [0, 0]
        loc2 = [100, 100]
        loc3 = [1280, 800]
        self.assertTrue(self.cam.pointer_game_space(self.window, loc1) == [640, 400],
                        "Test 1.1 failed")
        self.assertTrue(self.cam.pointer_game_space(self.window, loc2) == [540, 300],
                        "Test 1.2 failed")
        self.assertTrue(self.cam.pointer_game_space(self.window, loc3) == [-640, -400],
                        "Test 1.3 failed")

        self.cam.zoom_in(-.5)
        self.assertTrue(self.cam.pointer_game_space(self.window, loc1) == [1280, 800],
                        "Test 2.1 failed")
        self.assertTrue(self.cam.pointer_game_space(self.window, loc2) == [1080, 600],
                        "Test 2.2 failed")
        self.assertTrue(self.cam.pointer_game_space(self.window, loc3) == [-1280, -800],
                        "Test 2.3 failed")

        self.cam.zoom_in(1.1)
        self.assertTrue(self.cam.pointer_game_space(self.window, loc1) == [400, 250],
                        "Test 3.1 failed")
        self.assertTrue(self.cam.pointer_game_space(self.window, loc2) == [337.5, 187.5],
                        "Test 3.2 failed")
        self.assertTrue(self.cam.pointer_game_space(self.window, loc3) == [-400, -250],
                        "Test 3.3 failed")

    def test_level(self):
        """ """
        print("|\tRunning Level Tests...")
