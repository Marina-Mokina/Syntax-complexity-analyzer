from corpus_search import find_postcard_in_corpus
from analysis_result import AnalysisResult
from complexity_metrics import ComplexityMetrics
from dependency_parser import DependencyParser


def main():
    text = input("Введите текст для анализа: ")

    corpus_result = find_postcard_in_corpus(text)
    print(corpus_result)
    if corpus_result:
        print(f"Открытка найдена в корпусе")
        print(f"      Номер: #{corpus_result['id']}")
        print(f"      Дата: {corpus_result['date']}")
        print(f"      Тег: {corpus_result['tag']}")
    else:
        print("Не найдено в корпусе")

    metrics_analyzer = ComplexityMetrics()
    parser = DependencyParser()

    metrics = metrics_analyzer.calculate_metrics(text)
    features = parser.get_features(text)

    result = AnalysisResult(text, metrics, features, parser)
    result.display()


if __name__ == "__main__":
    main()
