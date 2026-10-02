import unittest
from logic import add, subtract, multiply, divide

class TestCalculatorLogic(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add(2, 3), 5)
    
    def test_subtract(self):
        self.assertEqual(subtract(5, 3), 2)
        
    def test_multiply(self):
        self.assertEqual(multiply(2, 3), 6)
        
    def test_divide(self):
        self.assertEqual(divide(6, 3), 2)
        
    def test_divide_by_zero(self):
        with self.assertRaises(ZeroDivisionError):
            divide(5, 0)

if __name__ == '__main__':
    unittest.main()
