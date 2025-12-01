from .analysis_result import AnalysisResult
from .complexity_metrics import ComplexityMetrics

# from .dependency_parser import DependencyParser


def main():
    """
    Prompts user for text input, analyzes complexity metrics, and displays the results
    """
    text = input("Text for analysis: ")
    metrics_analyser = ComplexityMetrics()
    metrics = metrics_analyser.calculate_metrics(text)
    features = {}
    result = AnalysisResult(text, metrics, features)
    result.display()


if __name__ == "__main__":
    main()
