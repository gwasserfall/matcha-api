import unittest


class TestMatchaSignUp(unittest.TestCase):

    def setUp(self):
		self.base_url = "http://localhost:5000"

    def test_sum(self):
        response = requests.get("{0}".format(self.base_url))

        


        self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")

    def test_sum_tuple(self):
        self.assertEqual(sum((1, 2, 2)), 6, "Should be 6")

if __name__ == '__main__':
    unittest.main()