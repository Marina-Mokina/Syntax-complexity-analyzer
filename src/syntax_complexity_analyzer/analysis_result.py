class AnalysisResult:
    """Represents and displays text analysis results"""

    def __init__(self, text: str, complexity_metrics: 'ComplexityMetrics', dependency_parser: 'DependencyParser'):
        """
        Initialize AnalysisResult with text and analyzer objects

        Args:
            text (str): Original input text for analysis
            complexity_metrics (ComplexityMetrics): Object containing readability metrics
            dependency_parser (DependencyParser): Object containing syntactic analysis results
        """
        self.text = text
        self.complexity = complexity_metrics
        self.parser = dependency_parser

    def display(self) -> None:
        """Displays complete analysis results in console with clear structure"""

        print("Отчет по анализу уровня сложности текста\n")

        print("1. Метрики удобочитаемости")

        avg_sentence_length = self.complexity._avg_sentence_length()
        avg_word_length = self.complexity._avg_word_length()
        fres = self.complexity._calculate_readability_score(avg_sentence_length, avg_word_length)

        print(f"    Средняя длина предложения в словах: {avg_sentence_length:.2f}")
        print(f"    Среднее длина слова в слогах: {avg_word_length:.2f}")
        print(f"    Индекс удобочитаемости Флеша (FRES): {fres:.2f}")

        print("Оценка уровня читаемости:")
        complexity_level = self.complexity.determine_complexity(fres)
        print(complexity_level)

        print("\n2. Синтаксические характеристики")

        if self.parser:
            tree_depth = self.parser.calculate_tree_depth()
            subordinate_clauses = self.parser.count_subordinate_clauses()
            max_dependency_distance = self.parser.calculate_max_dependency_distance()
            avg_children = self.parser.calculate_avg_children()

            print(f"    Максимальная глубина дерева зависимостей: {tree_depth}")
            print(f"    Количество придаточных предложений: {subordinate_clauses}")
            print(f"    Максимальное расстояние зависимостей: {max_dependency_distance}")
            print(f"    Среднее количество детей на токен: {avg_children:.2f}")

        print("\n3. Дерево зависимостей")

        if self.parser:
            tree_visualization = self.parser.get_tree_visualization()
            print(tree_visualization)
