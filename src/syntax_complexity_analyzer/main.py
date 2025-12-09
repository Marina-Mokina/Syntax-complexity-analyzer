from src.syntax_complexity_analyzer.corpus_search import CorpusSearch
from src.syntax_complexity_analyzer.analysis_result import AnalysisResult
from src.syntax_complexity_analyzer.complexity_metrics import ComplexityMetrics
from src.syntax_complexity_analyzer.dependency_parser import DependencyParser


def main():
    text = input('Введите текст для анализа: ')

    data = CorpusSearch(text)
    data.find_postcard_in_corpus()
    data.display_corpus_postcard()

    metrics_analyzer = ComplexityMetrics(text)
    parser = DependencyParser(text)

    result = AnalysisResult(text, metrics_analyzer, parser)
    result.display()


if __name__ == '__main__':
    main()
