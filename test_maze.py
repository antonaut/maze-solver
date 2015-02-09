import unittest
from maze import *

class mazetest(unittest.TestCase):

    def setUp(self):
        self.t1 = {
            'maze': [
                [1,0,1,1,1,1,1,1,1,1],
                [1,0,1,1,1,1,1,1,1,1],
                [1,0,0,0,0,0,0,0,0,1],
                [1,1,1,1,1,1,1,1,0,1]
            ],
            'start':(1, 0),
            'end':(8, 3)
        }

    def test_solve(self):
        print solve(self.t1.get('maze'), self.t1.get('start'), self.t1.get('end'))

if __name__ == '__main__':
    unittest.main()
