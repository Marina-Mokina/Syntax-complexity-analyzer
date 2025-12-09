from corpus_search import CorpusSearch
from analysis_result import AnalysisResult
from complexity_metrics import ComplexityMetrics
from dependency_parser import DependencyParser


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
