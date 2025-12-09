import unittest
from src.syntax_complexity_analyzer.complexity_metrics import ComplexityMetrics


class TestComplexityMetrics(unittest.TestCase):
    def test_avg_sentence_length_simple_case(self):
        text = 'Дело было в январе, стояла елка на горе, а возле этой елки бродили злые волки.'
        expected_avg_len = 15.00
        actual_avg_len = ComplexityMetrics(text)._avg_sentence_length()
        self.assertEqual(actual_avg_len, expected_avg_len)

    def test_avg_word_length_simple_case(self):
        text = 'Дело было в январе, стояла елка на горе, а возле этой елки бродили злые волки.'
        expected_avg_len = 2.07
        actual_avg_len = ComplexityMetrics(text)._avg_word_length()
        self.assertEqual(actual_avg_len, expected_avg_len)

    def test_calculate_readability_score_simple_case(self):
        text = 'Дело было в январе, стояла елка на горе, а возле этой елки бродили злые волки.'
        avg_sent_len = 15.00
        avg_word_len = 2.07
        expected_fres = 206.835 - 1.3 * 15.00 - 60.1 * 2.07
        actual_fres = ComplexityMetrics(text)._calculate_readability_score(avg_sent_len, avg_word_len)
        self.assertEqual(actual_fres, expected_fres)

    def test_determine_complexity_very_difficult(self):
        text = 'Дело было в январе, стояла елка на горе, а возле этой елки бродили злые волки.'
        result = ComplexityMetrics(text).determine_complexity(49.10)
        expected_result = "Уровень: Студент вуза. Сложный для чтения"
        self.assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()
