import unittest
from src.syntax_complexity_analyzer.dependency_parser import DependencyParser
from natasha import Doc


class TestDependencyParser(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.parser = DependencyParser("Дело было в январе, стояла елка на горе, а возле этой елки бродили злые волки.")

    def test_parse_text(self):
        self.assertIsInstance(self.parser.doc, Doc)

    def test_calculate_tree_depth(self):
        expected_depth = 3
        actual_depth = self.parser.calculate_tree_depth()
        self.assertEqual(expected_depth, actual_depth)

    def test_count_subordinate_clauses(self):
        expected_subordinate_clauses = 0
        actual_subordinate_clauses = self.parser.count_subordinate_clauses()
        self.assertEqual(expected_subordinate_clauses, actual_subordinate_clauses)

    def test_calculate_max_dependency_distance(self):
        expected_max_dependency_distance = 15
        actual_max_dependency_distance = self.parser.calculate_max_dependency_distance()
        self.assertEqual(expected_max_dependency_distance, actual_max_dependency_distance)

    def test_calculate_avg_children(self):
        expected_avg_children = 1.00
        actual_avg_children = self.parser.calculate_avg_children()
        self.assertAlmostEqual(expected_avg_children, actual_avg_children, places=1)

    def test_get_tree_visualization(self):
        visualization = self.parser.get_tree_visualization()
        self.assertTrue(isinstance(visualization, str))
        self.assertIn('Sentence ', visualization)


if __name__ == '__main__':
    unittest.main()
