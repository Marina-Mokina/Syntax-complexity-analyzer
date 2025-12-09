import unittest
from complexity_metrics import ComplexityMetrics


class TestComplexityMetrics(unittest.TestCase):
    def test_avg_sentence_length_simple_case(self):
        expected_avg_len = 4
        actual_avg_len = ComplexityMetrics(text="Мама мыла раму.")._avg_sentence_length()
        self.assertEqual(actual_avg_len, expected_avg_len)

    def test_avg_word_length_simple_case(self):
        expected_avg_len = 2
        actual_avg_len = ComplexityMetrics(text="Мама мыла раму.")._avg_word_length()
        self.assertEqual(actual_avg_len, expected_avg_len)

    def test_calculate_readability_score_simple_case(self):
        # Проверяем расчёт индекса удобочитаемости (FRES)
        avg_sent_len = 4
        avg_word_len = 3
        expected_fres = 206.835 - 1.3 * 4 - 60.1 * 2
        actual_fres = ComplexityMetrics(text="Мама мыла раму.")._calculate_readability_score(avg_sent_len, avg_word_len)
        self.assertEqual(actual_fres, expected_fres)

    def test_determine_complexity_very_difficult(self):
        # Проверяем сложность текста при низких показателях удобочитаемости
        result = ComplexityMetrics(text="Мама мыла раму.").determine_complexity(81)
        expected_result = "Уровень: Ученик 6 класса. Легкий для чтения"
        self.assertEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()
